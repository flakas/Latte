#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from progress.bar import Bar
from latte.db import Log, Tag
from latte.trackers import TagTracker

class Tags(object):
    """ Manages CRUD actions for log tags """

    def __init__(self, config, db, args):
        self.config = config
        self.db = db
        self.args = args
        self.tracker = TagTracker(self.db)

    def run(self):
        if self.args.subcommand == 'retag':
            self.retag()
        elif self.args.subcommand == 'add':
            self.add()
        elif self.args.subcommand == 'delete':
            self.delete()
        elif self.args.subcommand == 'show':
            self.show()
        else:
            raise NotImplementedError("Tags command not implemented")

    def add(self):
        """ Create a new tag to be tracked """
        options = {}
        for prop_name in ['window_title', 'window_class', 'window_instance', 'tag']:
            if self.args.__getattribute__(prop_name):
                options[prop_name] = self.args.__getattribute__(prop_name)

        tag = Tag(name=self.args.name)
        tag.set_options(options)

        self.db.add(tag)
        self.db.commit()

    def delete(self):
        """ Delete an existing tag by name """
        tag = self.db.query(Tag).filter(Tag.name == self.args.name).first()
        if not tag:
            sys.exit(f'Tag "{self.args.name}" not found')

        self.db.delete(tag)
        self.db.commit()

    def show(self):
        """ Show all tags and their configurations """
        tags = self.db.query(Tag).all()
        print(f'Total tags: {len(tags)}')
        for (i, tag) in enumerate(tags):
            options = tag.get_options()
            options = ', '.join([': '.join([k, v]) for (k, v) in options.items()])
            print(f"{i}) {tag.name}: {options}")

    def retag(self, commit_frequency=10000):
        """ Retag all existing logs with existing tags """
        all_logs = self.db.query(Log).all()
        bar = Bar('Retagging logs', max=len(all_logs), suffix = '%(percent).1f%%, Elapsed: %(elapsed)ds, Remaining: %(eta)ds')
        for (i, log) in enumerate(all_logs):
            log.tags.clear()
            self.tracker.track(log)
            if i % commit_frequency == 0:
                self.db.commit()
            bar.next()
        self.db.commit()
        bar.finish()
