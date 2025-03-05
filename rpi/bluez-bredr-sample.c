#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/socket.h>
#include <bluetooth/bluetooth.h>
#include <bluetooth/hci.h>
#include <bluetooth/hci_lib.h>
#include <bluetooth/rfcomm.h>

// Function to scan for BR/EDR devices
void scan_for_devices() {
    inquiry_info *devices = NULL;
    int max_devices = 255;  // Maximum number of devices we can discover
    int num_devices;        // Actual number of devices discovered
    int device_id, socket;  // Device ID and socket for the Bluetooth adapter
    int i;
    char addr[19] = { 0 };  // Bluetooth address string (e.g., "XX:XX:XX:XX:XX:XX")
    char name[248] = { 0 }; // Device name

    // Get the ID of the first available Bluetooth adapter
    device_id = hci_get_route(NULL);
    if (device_id < 0) {
        perror("No Bluetooth adapter available");
        exit(1);
    }

    // Open a socket to the Bluetooth adapter
    socket = hci_open_dev(device_id);
    if (socket < 0) {
        perror("Unable to open socket to Bluetooth adapter");
        exit(1);
    }

    // Allocate memory for the inquiry results
    devices = malloc(max_devices * sizeof(inquiry_info));
    if (devices == NULL) {
        perror("Out of memory");
        exit(1);
    }

    // Perform device discovery
    // Parameters: socket, inquiry length (1.28s * 8 = 10.24s), max devices, flags, devices array
    printf("Scanning for BR/EDR devices...\n");
    num_devices = hci_inquiry(device_id, 8, max_devices, NULL, &devices, IREQ_CACHE_FLUSH);
    if (num_devices < 0) {
        perror("Inquiry failed");
        exit(1);
    }

    // Display discovered devices
    printf("Found %d device(s)\n", num_devices);
    for (i = 0; i < num_devices; i++) {
        // Convert Bluetooth address to string
        ba2str(&(devices+i)->bdaddr, addr);
        
        // Get device name
        memset(name, 0, sizeof(name));
        if (hci_read_remote_name(socket, &(devices+i)->bdaddr, sizeof(name), name, 0) < 0) {
            strcpy(name, "[unknown]");
        }
        
        printf("%d. %s - %s\n", i+1, addr, name);
    }

    free(devices);
    close(socket);
}

// Function to connect to a device using RFCOMM
int connect_rfcomm(const char* target_addr, int channel) {
    struct sockaddr_rc addr = { 0 };
    int sock;
    bdaddr_t bdaddr;

    // Convert address string to Bluetooth address
    str2ba(target_addr, &bdaddr);

    // Allocate a socket
    sock = socket(AF_BLUETOOTH, SOCK_STREAM, BTPROTO_RFCOMM);
    if (sock < 0) {
        perror("Socket creation failed");
        return -1;
    }

    // Set the connection parameters
    addr.rc_family = AF_BLUETOOTH;
    addr.rc_channel = channel;
    memcpy(&addr.rc_bdaddr, &bdaddr, sizeof(bdaddr_t));

    // Connect to the device
    printf("Connecting to %s on channel %d...\n", target_addr, channel);
    if (connect(sock, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
        perror("Connection failed");
        close(sock);
        return -1;
    }

    printf("Connected successfully\n");
    return sock;
}

// Function to send data over RFCOMM connection
int send_data(int sock, const char* data) {
    int bytes_sent;
    
    printf("Sending: %s\n", data);
    bytes_sent = write(sock, data, strlen(data));
    if (bytes_sent < 0) {
        perror("Send failed");
        return -1;
    }
    
    printf("Sent %d bytes\n", bytes_sent);
    return bytes_sent;
}

// Function to receive data over RFCOMM connection
int receive_data(int sock, char* buffer, int buffer_size) {
    int bytes_read;
    
    memset(buffer, 0, buffer_size);
    bytes_read = read(sock, buffer, buffer_size - 1);
    if (bytes_read < 0) {
        perror("Receive failed");
        return -1;
    }
    
    printf("Received %d bytes: %s\n", bytes_read, buffer);
    return bytes_read;
}

// Function to create an RFCOMM server
int create_rfcomm_server(int channel) {
    struct sockaddr_rc loc_addr = { 0 };
    int sock, client, bytes_read;
    socklen_t opt = sizeof(loc_addr);
    char buffer[1024] = { 0 };

    // Allocate socket
    sock = socket(AF_BLUETOOTH, SOCK_STREAM, BTPROTO_RFCOMM);
    if (sock < 0) {
        perror("Socket creation failed");
        return -1;
    }

    // Bind socket to the first available Bluetooth adapter
    loc_addr.rc_family = AF_BLUETOOTH;
    loc_addr.rc_bdaddr = *BDADDR_ANY;
    loc_addr.rc_channel = channel;

    if (bind(sock, (struct sockaddr *)&loc_addr, sizeof(loc_addr)) < 0) {
        perror("Binding failed");
        close(sock);
        return -1;
    }

    // Listen for connections
    if (listen(sock, 1) < 0) {
        perror("Listen failed");
        close(sock);
        return -1;
    }

    printf("Listening for connections on channel %d...\n", channel);
    
    // This is just the server socket - the actual accepting of connections 
    // would happen in the main loop of your application
    return sock;
}

// Sample main function showing usage
int main(int argc, char **argv) {
    int choice;
    char target_addr[19];
    int channel;
    int sock;
    char buffer[1024];

    printf("BlueZ BR/EDR Sample\n");
    printf("1. Scan for devices\n");
    printf("2. Connect to device\n");
    printf("3. Create RFCOMM server\n");
    printf("Enter choice (1-3): ");
    scanf("%d", &choice);

    switch (choice) {
        case 1:
            scan_for_devices();
            break;
            
        case 2:
            printf("Enter device address (XX:XX:XX:XX:XX:XX): ");
            scanf("%18s", target_addr);
            printf("Enter RFCOMM channel (typically 1): ");
            scanf("%d", &channel);
            
            sock = connect_rfcomm(target_addr, channel);
            if (sock >= 0) {
                // Send sample data
                send_data(sock, "Hello from BlueZ BR/EDR client!");
                
                // Receive response
                receive_data(sock, buffer, sizeof(buffer));
                
                // Close the connection
                close(sock);
            }
            break;
            
        case 3:
            printf("Enter channel to listen on (typically 1): ");
            scanf("%d", &channel);
            
            sock = create_rfcomm_server(channel);
            if (sock >= 0) {
                printf("Server started. Press Enter to exit...");
                getchar(); // Consume newline from previous scanf
                getchar(); // Wait for Enter
                close(sock);
            }
            break;
            
        default:
            printf("Invalid choice\n");
    }

    return 0;
}
