# Web UI for IDK Fuzzer

### Steps
- Download and install Node.js from https://nodejs.org/en/download/.
- Run `npm install` to install the dependencies.
- Run `npm install nodemon -g` to install nodemon as global.
- Now run `nodemon app`.
- Webpage will be live at `localhost:1337`.

All Uploaded files will be under ./uploads

### Updating entries

`testCases` have to be update during the execution of the job and `active` have to updated once the job is finished. To do this, send a get request to `localhost:1337/update`. Attach a query to denote which entry have to be updated. Format is `?job=name&entry=entryname&value=value` where `job` is the jobName in the db. `entry` is the entry to be updated and `value` is the value you want to set. Setting `active` to false will set the end date and time. No need to set them seperately.

Example of updating active to false:

`http://localhost:1337/update?job=Sourag&entry=active&value=false`