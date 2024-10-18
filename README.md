# evernote2md

## Introduction

This is a simple command line tool that can be used to extract journal
entries from [Evernote](https://evernote.com) and turn them into a
collection of Markdown files. In this tool's case the Markdown collection is
built so it can easily be used as an [Obsidian](https://obsidian.md) Vault.

Note that I wrote this tool with a very specific job in mind, for myself, so
there are a couple of hard-coded things going on inside it (especially when
it comes to some tidying up of tags). I may turn such things into
configuration options in the future, but keep this in mind and be prepared
to modify the code to taste if you have a use for this.

## Installing

### pipx

The package can be installed using [`pipx`](https://pypa.github.io/pipx/):

```sh
$ pipx install evernote2md
```

### Homebrew

The package is available via Homebrew. Use the following commands to install:

```sh
$ brew tap davep/homebrew
$ brew install evernote2md
```

## Usage

### Getting ready to use

The first thing you will need to do is create an export of your Evernote
notebook. I honestly can't remember the method, but it's whatever results in
you having a zip file full of HTML files and directories containing
attachments.

### Assumptions for the "Vault"

As mentioned earlier, this tool assumes that you're going to be making an
Obsidian Vault with the resulting Markdown. With this in mind the tool makes
the following assumptions:

- You wish to have a `YYYY/MM/DD` folder hierarchy for the entries.
- You prefer to have all attachments held in a `attachments` folder below
  the location of the entry the attachments are for.

These are my preferences, if yours differ it should be simple enough to
modify the code to taste (or, if what you prefer seems like it could be a
reasonable configuration option, create an issue in the repo and tell me all
about it).

### Create the target "Vault"

Create a directory where the "Vault" will be created. Note that `evernote2md`
creates all directories and files *within* this directory.

### Perform the conversion

With all the above done and in mind, run the tool like this:

```sh
evernote2md evernote-data markdown-vault
```

where `evernote-data` is the path to the directory that holds all of the
extracted Evernote files, and where `markdown-vault` is the directory you
created that will be the Vault.

## Getting help

If you need help please feel free to [raise an
issue](https://github.com/davep/evernote2md/issues).

[//]: # (README.md ends here)
