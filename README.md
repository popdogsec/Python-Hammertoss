# Python-Hammertoss
This is a piece of command and control software that draws inspiration from the HAMMERTOSS malware utilized by APT29 written in Python. It includes 2 scripts, one to aid the attacker in deploying the commands and the other to control the remote victim. The script to be implanted can be compiled with auto-py-to-exe and when compiled in a windowless fashion does not alert the victim that it has begun running.

The heart of this project was to implement a way to deploy commands stealthily over normal web traffic by utilizing steganography. The fetch process for instructions by the victim machine is nothing more than requesting a few social media pages, making it very easy to go unnoticed.

It should go without saying that this shouldn't be used with out the targets consent. Under no circumstances should this be used in any unlawful way.

DEMO:
https://www.youtube.com/watch?v=PQdnS4abGFk

