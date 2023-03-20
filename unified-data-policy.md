# Unified data policy

## Replication policies

- Level 4: at least 4 copies, in 3 location, 2 countries, 2 continents. 

- Level 3: at least 3 copies, in 2 location, 2 countries. 

- Level 2: at least 2 copies. 

- Level 1: at least 1 copies. 

## Confidential Policies

> `sensitive` means I don't want to leak it, `important` means I don't want to lost it. 

- type D: non-sensitive important data, such as environent setup script, software installation packs, saved movies, ...

- type I: public personal data, or non-important public data. 

- type N2: sensitive important personal data, such as photos, development, game save...

- type N1: sensitive non-important personal data, such as system logs, chat logs, screenshots, web history, development environment, ...

- type M: secret keys/seeds/passwords, server userdata... 

- type MX: GPG masterkey itself. 

- [TODO]X

> **super key doesn't not apply any data policy, and FORBIDDEN to save on ANY medium.** 

|Type|Encryption|Ownership|Replication|Current\_Solution|
|---|---|---|---|---|
|M|Always, by GPG master key or super key|First-party|Level 4|extraDisk/.backup/typeM|
|MX|Always, by cold key and super key|First-party|Level 4|extraDisk/.backup/typeM/gpg-masterkey.tar.gz.gpg|
|N2|Always|First-party or Third-party|Level 3|~/extraDisk/.backup|
|N1|Always|First-party or Third-party|Level 1|normal encrypted devices|
|D|Optional|First-party or Third-party|Level 2|nfs/rpc\_downloads|
|I|Optional|First-party or Third-party|Level 1|normal devices|

|Properties|Important|Non-Important|
|---|---|---|
|Sensitive|MX,M,N2|N1|
|Non-sensitive|D|I|

All device storing / processing unencrypted sensitive data, must either using Fully-Open-Source-Software, or be disconnected from Internet and destroyed afterward. 
