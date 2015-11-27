# calvinbookshelf-db

This repository holds mongodb backups of our `books` and `classes` collections.

## Installing MongoDB CLI Tools

* [Install on Linux](https://docs.mongodb.org/manual/administration/install-on-linux/)
* [Install on OSX](https://docs.mongodb.org/manual/tutorial/install-mongodb-on-os-x/)
* [Install on Windows](https://docs.mongodb.org/manual/tutorial/install-mongodb-on-windows/)

## Restoring From Backup Collections

To add these dumps to your meteor application, make sure that meteor is running, then 
enter this `mongorestore` command:

```bash
mongorestore -h 127.0.0.1 --port 3001 --drop -d meteor <path/to/backups/directory>
```
