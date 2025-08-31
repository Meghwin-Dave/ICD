# ICD - Container Management System
## User Documentation

### 1. Overview

The ICD (Inland Container Depot) app is a comprehensive container management and logistics system designed to streamline the handling of shipping containers throughout their lifecycle. This system manages container movements, storage, services, and documentation from arrival at the port to final delivery.

**Key Features:**
- Container tracking and management
- Manifest processing and vessel information
- Service order management
- Gate pass generation and control
- Container movement and location tracking
- Storage charge calculations
- Document management and workflow

**Target Users:**
- Port operators and terminal staff
- Shipping line representatives
- Clearing agents and freight forwarders
- Transport companies
- Customs officials

---

### 2. User Flow

#### 2.1 Container Arrival Process
```
Vessel Arrives → Manifest Upload → Container Reception → Container Details Creation → Location Assignment
```

#### 2.2 Service Request Process
```
Service Order Creation → Service Details → Approval → Service Execution → Completion
```

#### 2.3 Container Movement Process
```
Movement Order → Location Update → Movement Execution → Status Update
```

#### 2.4 Container Exit Process
```
Gate Pass Generation → Container Inspection → Exit Authorization → Container Release
```

#### 2.5 Complete Workflow
```
Login → Dashboard → Select Operation → Create/Update Documents → Submit → Track Status → Generate Reports
```

---

### 3. Doctype-wise Documentation

#### 3.1 Manifest
**Purpose:** Records vessel arrival information and container manifests for customs and port operations.

**Key Fields:**
- **Upload Manifest:** Attach the vessel manifest file
- **MRN:** Movement Reference Number
- **Vessel Name:** Name of the arriving vessel
- **Call Sign:** Vessel's radio call sign
- **Voyage:** Voyage number
- **TPA UID:** Terminal Port Authority Unique Identifier
- **Arrival Date:** Date of vessel arrival
- **Port:** Port of arrival (TEAGTL/DP World)

**How to Use:**
1. Navigate to Manifest from the ICD module
2. Click "New" to create a new manifest
3. Upload the vessel manifest file
4. Fill in vessel information (name, call sign, voyage, etc.)
5. Add container details in the containers section
6. Submit the manifest

**Typical Workflow:**
- Creation → Vessel information entry → Container details → Submission → Customs processing

**Example Use Case:** Recording arrival of vessel "MSC OSCAR" with 500 containers at TEAGTL port.

---

#### 3.2 Container Details
**Purpose:** Comprehensive container information management including specifications, location, and billing details.

**Key Fields:**
- **Container Information:**
  - M B/L No: Master Bill of Lading number
  - Container No: Unique container identifier
  - Type of Container: Container type (GP, RF, OT, etc.)
  - Size (ft): Container dimensions
  - Cargo Type: Type of goods being transported
  - Seal Numbers: Container seal identifiers

- **Location & Movement:**
  - Current Location: Present container location
  - Status: Current container status
  - Arrival Date: Date container arrived
  - Received Date: Date container was received

- **Billing Details:**
  - Total Days: Total days in storage
  - Free Days: Days without charges
  - Billable Days: Days subject to charges
  - Storage Charges: Applicable storage fees

**How to Use:**
1. Create container details when container is received
2. Update location and status as container moves
3. Monitor storage days and charges
4. Link to related documents (manifest, service orders)

**Typical Workflow:**
- Creation → Location assignment → Status updates → Movement tracking → Billing calculation

**Example Use Case:** Tracking container TCLU1234567 from arrival through various locations until final delivery.

---

#### 3.3 Service Order
**Purpose:** Manages requests for container-related services like cleaning, inspection, or special handling.

**Key Fields:**
- **Company Information:**
  - C and F Company: Cleaning and Forwarding company
  - Clearing Agent: Customs clearing agent
  - Consignee: Container recipient

- **Container Information:**
  - Container ID: Link to container details
  - M B/L No: Master Bill of Lading number
  - Container No: Container identifier
  - Container Size: Container dimensions

- **Service Details:**
  - Service: Table of requested services
  - Posting DateTime: When service was requested

**How to Use:**
1. Create service order for specific container
2. Select required services from service table
3. Assign to appropriate service providers
4. Track service completion status

**Typical Workflow:**
- Creation → Service specification → Provider assignment → Service execution → Completion

**Example Use Case:** Requesting container cleaning and inspection services for container ABC123.

---

#### 3.4 Container Reception
**Purpose:** Records the formal reception of containers at the terminal or depot.

**Key Fields:**
- **Reception Details:**
  - Container ID: Link to container details
  - Reception Date: Date container was received
  - Reception Location: Where container was received
  - Reception Status: Current reception status

**How to Use:**
1. Create reception record when container arrives
2. Verify container condition and seals
3. Assign initial location
4. Update container status

**Typical Workflow:**
- Container arrival → Reception creation → Inspection → Location assignment → Status update

**Example Use Case:** Recording reception of 20 containers from vessel "EVER GIVEN" at berth 3.

---

#### 3.5 Container Movement Order
**Purpose:** Authorizes and tracks container movements within the terminal or between locations.

**Key Fields:**
- **Movement Details:**
  - Container ID: Container to be moved
  - From Location: Current location
  - To Location: Destination location
  - Movement Type: Type of movement required
  - Movement Date: When movement should occur

**How to Use:**
1. Create movement order for container relocation
2. Specify source and destination locations
3. Assign to transport team
4. Track movement execution

**Typical Workflow:**
- Movement request → Order creation → Transport assignment → Movement execution → Status update

**Example Use Case:** Moving container XYZ789 from storage yard A to loading area B for truck pickup.

---

#### 3.6 Gate Pass
**Purpose:** Controls container exit from the terminal and tracks final delivery.

**Key Fields:**
- **Container Information:**
  - Container ID: Container being released
  - Container No: Container identifier
  - Size: Container dimensions
  - Seal No: Container seal number

- **Transport Details:**
  - Transporter: Transport company
  - Truck: Vehicle information
  - Driver: Driver details
  - License No: Driver's license number

- **Exit Details:**
  - Exit Date: When container left terminal
  - Exit Location: Gate used for exit

**How to Use:**
1. Generate gate pass when container is ready for delivery
2. Verify all documentation is complete
3. Inspect container condition
4. Authorize exit and track delivery

**Typical Workflow:**
- Exit request → Gate pass generation → Container inspection → Exit authorization → Delivery tracking

**Example Use Case:** Releasing container DEF456 to ABC Transport for delivery to consignee warehouse.

---

#### 3.7 Supporting Doctypes

**Cleaning and Forward Company:**
- Manages companies providing cleaning and forwarding services
- Stores contact information and service capabilities

**Clearing Agent:**
- Records customs clearing agents
- Maintains agent credentials and contact details

**Consignee:**
- Stores consignee information
- Links to container deliveries and billing

**Transporter:**
- Manages transport companies
- Tracks vehicle and driver information

**Security Officer:**
- Records security personnel
- Manages access control and inspections

---

### 4. Integration and Dependencies

#### 4.1 Document Relationships
```
Manifest → Container Details → Container Reception → Service Orders → Container Movement Orders → Gate Pass
```

#### 4.2 Data Flow
1. **Manifest Creation:** Establishes vessel and container baseline information
2. **Container Reception:** Links containers to manifest and creates detailed records
3. **Service Orders:** Request services for specific containers
4. **Movement Orders:** Track container location changes
5. **Gate Pass:** Final exit documentation

#### 4.3 Key Dependencies
- Container Details must reference a Manifest
- Service Orders must link to Container Details
- Movement Orders require Container Details
- Gate Pass must reference Container Details and Manifest

---

### 5. Tips and Common Actions

#### 5.1 Quick Tips
- **Use Filters:** Apply filters in list views to find specific containers or documents quickly
- **Search by Container No:** Use container number for fastest document lookup
- **Check Status:** Always verify container status before creating related documents
- **Update Location:** Keep container location current for accurate tracking

#### 5.2 Common Actions
- **Daily Operations:**
  - Check dashboard for pending tasks
  - Review containers due for movement
  - Process service order requests
  - Generate daily reports

- **Weekly Tasks:**
  - Review storage charges
  - Update container statuses
  - Verify manifest completeness
  - Check service order completion

#### 5.3 Common Mistakes to Avoid
- **Don't forget to update container location** after movement
- **Don't submit documents** without verifying all required fields
- **Don't ignore storage day calculations** for billing accuracy
- **Don't create duplicate records** - always search existing documents first

#### 5.4 Keyboard Shortcuts
- **Ctrl + N:** Create new document
- **Ctrl + S:** Save document
- **Ctrl + Enter:** Submit document
- **Ctrl + F:** Find in current document
- **Ctrl + Shift + F:** Search across all documents

---

### 6. Reporting and Analytics

#### 6.1 Available Reports
- **Container Status Report:** Current location and status of all containers
- **Storage Charges Report:** Billing information for stored containers
- **Movement History Report:** Complete container movement timeline
- **Service Order Summary:** Pending and completed services
- **Gate Pass Report:** Container exit and delivery tracking

#### 6.2 Dashboard Features
- **Pending Tasks:** Quick view of items requiring attention
- **Container Count:** Total containers by status and location
- **Recent Activities:** Latest document updates and movements
- **Performance Metrics:** Key operational indicators

---

### 7. Troubleshooting

#### 7.1 Common Issues
- **Container not found:** Check if container number is entered correctly
- **Document submission failed:** Verify all required fields are filled
- **Location update error:** Ensure container exists and is not in transit
- **Service order creation failed:** Check if container is available for services

#### 7.2 Getting Help
- **System Administrator:** For technical issues and user access
- **Module Manager:** For business process questions
- **User Manual:** Reference this documentation for procedures
- **Training:** Contact your system administrator for additional training

---

### 8. Best Practices

#### 8.1 Data Entry
- **Accuracy First:** Double-check all container numbers and dates
- **Complete Information:** Fill all required fields before submission
- **Regular Updates:** Update container status and location promptly
- **Document Links:** Always maintain proper document relationships

#### 8.2 Workflow Management
- **Follow Sequence:** Complete documents in logical order
- **Status Tracking:** Monitor document status throughout process
- **Communication:** Coordinate with team members for smooth operations
- **Quality Control:** Review completed documents for accuracy

#### 8.3 Security
- **User Access:** Use only your assigned login credentials
- **Data Privacy:** Don't share sensitive container information
- **Logout:** Always log out when leaving your workstation
- **Password Security:** Use strong passwords and change regularly

---

This documentation provides a comprehensive guide to using the ICD Container Management System. For specific questions or additional training, please contact your system administrator or refer to the system help features.
