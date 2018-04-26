# 0.1.0 (February 19, 2016)
* Djacket is publicly released with these features:
    - User creation/deletion/settings
    - Repo creation/deletion/settings
    - Repo browsing/branches/commits/graphs
    - See other users public repos


# 0.2.0 (August 4, 2017)
* Djacket is dockerized.
    - All the development/production processes are now moved to Docker.
    - Lots of useless content is deleted.


# 0.2.1 (April 22, 2018)
* Minor fixes and updates.
    - NPM packages updated along with adding `package-lock.json` file.
    - `NodeJS` installation version changed to 8.x LTS.
    - `404` errors for icons fixed.
    - JS scripts modified for new versions of `jQuery` and `Chart.js`.
    - `TypeError: get_available_name() got an unexpected keyword argument 'max_length'` issue fixed.


# 0.2.2 (April 22, 2018)
* TravisCI configuration added.
    - Configuration for continuous integration in `Travis` build system added, regarding issue #10.


# 0.2.3 (April 27, 2018)
* Minor updates.
    - Configured `Django` logging for production.
    - Migrated from `Popen` to the new `run` function for calling system commands.
