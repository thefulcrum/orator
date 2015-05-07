# -*- coding: utf-8 -*-

import os
from cleo import InputOption, ListInput
from eloquent.migrations import Migrator, DatabaseMigrationRepository
from .base_command import BaseCommand


class RollbackCommand(BaseCommand):

    def configure(self):
        super(RollbackCommand, self).configure()

        self.set_name('migrate:rollback')
        self.set_description('Rollback the last database migration')
        self.add_option('database', 'd', InputOption.VALUE_OPTIONAL,
                        'The database connection to use')
        self.add_option('path', 'p', InputOption.VALUE_OPTIONAL,
                        'The path of migrations files to be executed.')
        self.add_option('pretend', 'P', InputOption.VALUE_NONE,
                        'Dump the SQL queries that would be run.')

    def execute(self, i, o):
        """
        Executes the command.

        :type i: cleo.inputs.input.Input
        :type o: cleo.outputs.output.Output
        """
        super(RollbackCommand, self).execute(i, o)

        dialog = self.get_helper('dialog')
        confirm = dialog.ask_confirmation(
            o,
            '<question>Are you sure you want to rollback the last migration?</question> ',
            False
        )
        if not confirm:
            return

        database = i.get_option('database')
        repository = DatabaseMigrationRepository(self._resolver, 'migrations')

        migrator = Migrator(repository, self._resolver)

        self._prepare_database(migrator, database, i, o)

        pretend = i.get_option('pretend')

        path = i.get_option('path')

        if path is None:
            path = self._get_migration_path()

        migrator.rollback(path, pretend)

        for note in migrator.get_notes():
            o.writeln(note)

    def _prepare_database(self, migrator, database, i, o):
        migrator.set_connection(database)
