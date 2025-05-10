# WebInterface-for-MySQL

A centralized database was implemented to store and manage user data in the access control and management system (ACS) under development. Such a base is necessary for:

1 Storage of unique identifiers (UIDS) of RFID cards of users;

2 Linking full names and photos for the facial recognition system;

3 Monitoring and administration of access;

4 Ensuring fast interaction of all system components — hardware (Arduino, RC522) and software (web interface, processing scripts).

Information from the database is used both to authorize access at the hardware level and to display the status of users in the monitoring system.

## 📌 Appointment

The MySQL database in this Access control and Management System (ACS) serves as the main repository of information about users, their IDs, and log-in/log-out history. It provides centralized data management, which is necessary for accurate identification, registration of access events, and linking RFID and biometric module data. This structure allows the system to remain reliable and scalable as the number of users and access points increases.

The database is used to quickly check the UID of RFID cards, compare them with the user's full name and other data, as well as store additional parameters such as photos for the face recognition system or access status (for example, temporarily blocked). The web interface interacting with the database allows administrators to flexibly manage accounts and receive information about access events in real time.

Additionally, MySQL provides the ability to backup, restore data, and secure a TLS connection. This makes it a suitable choice for building secure enterprise solutions where not only functionality and performance are important, but also compliance with information security requirements.

## ✅ Advantages of MySQL

- Reliability and fault tolerance. MySQL works stably under high loads, ensuring the safety and availability of data even in critical situations.

- Widespread distribution and support. The DBMS has an extensive community, many manuals and official documentation, which simplifies implementation and maintenance.

- High performance. MySQL is optimized for fast execution of sampling operations, which is critical when users have mass access to the database.

- Support for secure connections. The ability to use TLS connections provides protection against interception and modification of data on the network.

- Ease of integration. The database can be easily connected to backend applications on Flask and other web frameworks, and can also be used in conjunction with Keycloak or other IDM systems.

- Backup tools. The built-in tools allow you to set up regular backups and quickly restore data if necessary.

- Cross-platform. MySQL can be deployed on any OS, including Linux, Windows, and macOS.

## ⚠️ Disadvantages of MySQL

- It does not support some types of data from other databases. For example, there is no built-in support for JSONB, as in PostgreSQL.

- It is necessary to monitor the security manually. Despite TLS support, configuring secure access and rights management requires manual configuration.

- Depending on the correct setting. If the configuration is incorrect, performance problems or security vulnerabilities may occur.


## 📦 Database structure

To ensure reliable storage and processing of data about users of the access control and management system (ACS), a relational database structure based on MySQL was developed. This structure makes it possible to effectively manage information about identifiers, users, access events, and associated biometric data. MySQL ensures stable and scalable operation of the system that meets security and accessibility requirements.

Below is a diagram of the organization of tables used in the developed ACS.

![image](https://github.com/user-attachments/assets/9f0fd06d-eb4b-4388-b109-85455d11130a)

SQL code for creating a SKYD table in MySQL with the required fields:

```
CREATE TABLE SKYD (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    patronymic VARCHAR(100),
    rfid_tag VARCHAR(50) UNIQUE NOT NULL,
    photo VARCHAR(255)
);
```
- id — primary key with auto-increment;

- name — first name (you can combine the full name into one field if necessary);

- patronymic — patronymic (optional);

- rfid_tag is a unique RFID tag that must be filled in;
 
- photo — the name or path to the photo file.

## 🌐 A web interface for the administration of ACS

For the convenience of interacting with the access control and management system, a web interface has been developed that provides a fast and intuitive way to work with the user database. The interface is implemented using the Flask (Python) framework and HTML/CSS, which makes it a lightweight, scalable and cross-platform solution.

### 🔐 Login and password login

To ensure the security of the ACS system, an authorization process based on a username and password has been implemented. Users enter their credentials through a web form, after which the system verifies them on the server. Upon successful authentication, the user is granted access to the functionality, depending on their rights.

Password encryption is performed using reliable hashing methods such as bcrypt, which ensures data protection. A system has also been introduced to limit the number of login attempts to prevent password guessing attacks. The TLS protocol is used to protect the transmitted information, which eliminates the possibility of data interception.

![image](https://github.com/user-attachments/assets/a8af7914-60ac-4e21-8b0b-ffa2dc055846)

Сode on Flask that implements a simple login form with login and password verification.

[Login form in login_form.py file](login_form.py)

### 🔐 Authorization and security

Before accessing the functionality of the web interface, the user must complete the authorization procedure. This is necessary to restrict access to the administrative part of the system and prevent unauthorized changes. Authorization is implemented using secure password storage and session verification.

Additionally, TLS encryption is used to protect data during transmission between the client and the server. The thesis uses the TLS_AES_128_GCM_SHA256 cipher, which ensures the confidentiality, integrity and authenticity of the transmitted information. A self-signed certificate was also created to establish a secure HTTPS connection.

#### 🔐 Enabling TLS in MySQL

To protect the transmitted information between the MySQL server and the client application (the ACS web interface), TLS (Transport Layer Security) support was implemented in the graduation project. This allows you to encrypt data and prevent it from being intercepted by intruders.
📁 Step 1. Certificate generation

The following files were created to configure TLS:
1 ca.pem — certificate of the Certification Authority (CA)
2 server-cert.pem is a public MySQL server certificate
3 server-key.pem is the private key of the MySQL server

The creation can be done using OpenSSL:
```
openssl genrsa 2048 > ca-key.pem
openssl req -new -x509 -nodes -days 3650 -key ca-key.pem -out ca.pem

openssl req -newkey rsa:2048 -nodes -keyout server-key.pem -out server-req.pem
openssl x509 -req -in server-req.pem -days 3650 -CA ca.pem -CAkey ca-key.pem -set_serial 01 -out server-cert.pem

```

⚙️  Step 2. Configure my.cnf (or mysqld.cnf)

The parameters for enabling TLS have been added to the MySQL configuration file (/etc/mysql/my.cnf or /etc/mysql/mysql.conf.d/mysql.conf):

```
[mysqld]
ssl-ca=/etc/mysql/certs/ca.pem
ssl-cert=/etc/mysql/certs/server-cert.pem
ssl-key=/etc/mysql/certs/server-key.pem
require_secure_transport = ON
```
The path to the certificates is specified according to their location on the server.

The require_secure_transport = ON option forces clients to use TLS when connecting to the server.

🔄 Step 3. Restart MySQL

After changing the configuration, the server restarts.:

```
sudo systemctl restart mysql
```
The output should be:

![image](https://github.com/user-attachments/assets/e990c68f-b515-493e-a9c8-25f00088d1b8)

### 🧑‍💼 User Management

The interface allows you to:

- Add new users by specifying their full name and receiving a UID using an RFID reader;

- Automatically save the user's photo when added using the connected camera.;

- View existing users by displaying their ID, full name, UID, and photo;

- Edit or delete information if necessary.

Data is added via a simple HTML form, and the UID is read automatically when the RFID card is held up to the RC522 reader connected to the Arduino.

Fields for entering user data:

![image](https://github.com/user-attachments/assets/086f4b04-b5d2-472b-9e08-5e9e6f9e0953)

The HTML code of the corresponding form

[HTML code in add_users.html file](add_users.html)

Viewing data about entered users:

![image](https://github.com/user-attachments/assets/5912181f-e6b8-4bd8-aeb5-fb0032fd6516)

The HTML code of the corresponding form

[HTML code in view_users.html file](view_users.html)

### 📸 Integration with biometrics

For each user, you can add a photo to be used in the facial recognition system. After adding a user, the photo is saved in a specific directory, and the system automatically binds it to the UID.

### 🛠 Technical details

Server: Flask (Python)

Encryption: TLS (HTTPS)

Data storage: MySQL

RFID integration: through serialized exchange between Arduino and server

Photo support: via connected camera and OpenCV library

## 🌐 HTTPS web interface and certificate generation

To increase the security of interaction with the web interface of the access control system, the HTTPS protocol was configured, which provides data encryption between the server and the client. This prevented the possibility of intercepting confidential information such as usernames, passwords, and other data that could be transmitted while working with the system.

A self-signed SSL/TLS certificate was used to implement HTTPS on the server. This certificate is created to establish a secure connection and ensures that the data between the user and the server is encrypted. If a self-signed certificate is used, the browser notifies the user that the certificate has not been verified by a third party, but in the context of local and test systems, this is a sufficient security measure.

To generate a self-signed certificate and a private key for use in Flask with HTTPS,  use the openssl utility:

```
openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365 -nodes
```

After completing these steps, the received server.key (private key) and server.crt (certificate) files were used to configure HTTPS on the server.

![image](https://github.com/user-attachments/assets/dab493a4-efb4-477d-af0d-76abe80bf878)

This ensured the protection of all transmitted data, as well as increased user confidence in the system, ensuring that their data is protected during operation.

Below is the code for launching the Flask server using a self-signed TLS certificate:

```
if __name__ == '__main__':
    context = ('cert.pem', 'key.pem')  
    app.run(host='0.0.0.0', port=443, ssl_context=context)
```

# Authors
If you have any questions, you can ask them to us by writing to us at email:
- ivanovvvvvvvanton3829@gmail.com
