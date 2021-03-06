# encoding: utf-8
# -*- mode: ruby -*-
# vi: set ft=ruby :

# Hitchwiki Development Vagrant setup
# Using http://box.scotch.io/
#
# Modified from https://github.com/scotch-io/scotch-box/blob/master/Vagrantfile
# Added https://github.com/smdahlen/vagrant-hostmanager

require "yaml"
require "fileutils"

# Config file paths
current_dir = File.dirname(File.expand_path(__FILE__))
settings_file = "#{current_dir}/configs/vagrant.yaml"
settings_file_template = "#{current_dir}/configs/vagrant-example.yaml"

# Copy vagrant config file from template file if it doesn't exist yet
if not File.exist?(settings_file)
  FileUtils.cp(settings_file_template, settings_file)
end

# Load vagrant config file
settings = YAML.load_file(settings_file)

# Collect install arguments for the server install script
install_args = Array.new
install_args.push("--visualeditor") if settings["install_visualeditor"]
install_args.push("--ssl") if settings["setup_ssl"]

Vagrant.configure("2") do |config|

  config.hostmanager.enabled = settings["hostmanager_enabled"]
  config.hostmanager.manage_host = true
  config.hostmanager.ignore_private_ip = false
  config.hostmanager.include_offline = true

  config.vm.box = "scotch/box"
  config.vm.network "private_network", ip: settings["private_network_ip"]
  config.vm.hostname = settings["hostname"]

  # Run Mailcatcher on every `vagrant up`
  config.vm.provision "shell", inline: "/home/vagrant/.rbenv/shims/mailcatcher --http-ip=0.0.0.0", run: "always"

  # Install Hitchwiki with all of its dependencies
  # Uncomment the last part if you don't want to install VisualEditor & Parsoid
  config.vm.provision :shell, :path => "scripts/server_install.sh", :args => install_args

  config.vm.synced_folder ".", "/var/www", :mount_options => ["dmode=777", "fmode=755"]

end
