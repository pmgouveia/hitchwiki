# Hitchwiki
_The Hitchhiker's Guide to Hitchhiking the World_

[Hitchwiki](http://hitchwiki.org/) is a collaborative website for gathering information about [hitchhiking](http://hitchwiki.org/en/Hitchhiking) and other ways of extremely cheap ways of transport. It is maintained by many active hitchhikers all around the world. We have information about how to hitch out of big cities, how to cover long distances, maps and many more tips.

## How to help
This version is [currently under heavy development](https://love.hitchwiki.net/) in Turkey Dec 2014—Feb 2015 by [@simison](https://github.com/simison) and [@Remigr](https://github.com/Remigr/).

_[Contact us](http://hitchwiki.org/developers) if you want to join the effort!_

Read more about developing Hitchwiki [from the wiki](https://github.com/Hitchwiki/hitchwiki/wiki)

## Install & start hacking Hitchwiki

### Prerequisites
* Install [VirtualBox](https://www.virtualbox.org/) ([...because](http://docs.vagrantup.com/v2/virtualbox))
* Install [Vagrant](https://www.vagrantup.com/) ([docs](https://docs.vagrantup.com/v2/installation/))
* Make sure you have [`git`](http://git-scm.com/) in your system.

### Install
1. Clone the repo: `git clone https://github.com/Hitchwiki/hitchwiki.git && cd hitchwiki`
2. Start dev environment: `vagrant up`. This will run installation script on first launch.
3. Open [http://192.168.33.10/](http://192.168.33.10/) in your browser.

Suspend the virtual machine by typing `vagrant suspend`. When you're ready to begin working again, just run `vagrant up` again.

#### Install script will do the following:
* Download and extract [Mediawiki](https://www.mediawiki.org/)
* Install dependencies with Composer
* Create a database and configure MediaWiki
* Create three users

#### Pre-created users (user/pass)
* Admin: Hitchwiki / autobahn
* Bot: Hitchbot / autobahn
* User: Hitchhiker / autobahn

### Export Semantic structure
If you do changes to Semantic structures (forms, templates etc), you should export those files by running:
```bash
sh scripts/export.sh
```

Then notify others about changes so they know to update their project.

### Update
1. Pull latest changes: `git pull origin master`
2. Run update script: `sh ./scripts/update.sh`

## Vagrant box

We're using [Scotchbox](http://box.scotch.io/).

### SSH into Vagrant
```bash
vagrant ssh
```

### Database access
#### From the app
User: root
Pass: root
Host: localhost

#### From desktop
Only via SSH Forwarding.

User: root
Pass: root
Host: localhost
SSH Host: 192.168.33.10
SSH User: vagrant
SSH Password: vagrant

### Clean Vagrant box
If for some reason you want to have clean Scotchbox, database and MediaWiki installed, run:
```bash
vagrant destroy && vagrant up
```

### Update Vagrant box
Although not necessary, if you want to check for updates, just type:
```bash
vagrant box outdated
```

It will tell you if you are running the latest version or not of the box. If it says you aren't, simply run:
```bash
vagrant box update
```

## Setting up production environment
_TODO_

## License
Code [MIT](LICENSE.md)
Contents [Creative Commons](http://creativecommons.org/licenses/by-sa/4.0/)
