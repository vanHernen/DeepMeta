# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DeepMeta
                                 A QGIS plugin
 blabla
                              -------------------
        begin                : 2017-02-13
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Deep BV
        email                : jhe@deepbv.nl
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon, QFileDialog
from qgis.PyQt.QtWidgets import QWidget
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.utils import iface

# Initialize Qt resources from file resources.py
import resources
import subprocess
import urllib
import os
# Import the code for the dialog
from meta_data_dialog import DeepMetaDialog
import os.path


class DeepMeta:
    """QGIS Plugin Implementation."""
    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'DeepMeta_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)


        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Deep Metadata Generator')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'DeepMeta')
        self.toolbar.setObjectName(u'DeepMeta')


    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('DeepMeta', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """
        # Create the dialog (after translation) and keep reference
        self.dlg = DeepMetaDialog()

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToDatabaseMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/DeepMeta/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'MetaDataMaker'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginDatabaseMenu(
                self.tr(u'&Deep Metadata Generator'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

#    def getProject(self):
#        self.dlg.editmode.clear()
#        editmode = self.dlg.findChild(QLineEdit,"opdrg")
#       editmode.setText("abdcafd")

    def projFolderOpen(self):
        urlAdres = projectFolder
        self.dlg.opdrprojnr.setText(projectFolder)

    def select_input_file(self):
        global projectFolder
        global channels
        projectFolder = QFileDialog.getExistingDirectory(self.dlg, "Select directory", "T:\\")
        projectNumber = projectFolder[3:8]
        self.dlg.opdrg.setText(projectFolder)
#        self.dlg.projnr.setOpenExternalLinks(True)
#        urlAdres = projectFolder
#        urlAdres.replace(" ", "%20")
#        urlLink="<a href=" + urlAdres + "> <font face=verdana size=2 color=black>" + projectNumber + "</font> </a>"
#        subprocess.call("explorer " + LINK NAAR ADRES, shell=True)
#        subprocess.Popen(r'explorer /select,"C:\path\of\folder\file"')
#        self.dlg.projnr.setText(projectNumber)
        self.dlg.button.setText(projectNumber)
        #path = projectFolder
        dirList = os.listdir(projectFolder)
        dirs = []
        for i in dirList:
            dirs.append(i)
        dirs.sort()
        self.dlg.fwfolder.addItems(dirs)

    def run(self):
        """Run method that performs all the real work"""
#        button = self.dlg.findChild(QPushButton,"button")
        #button.clicked.disconnect()
#        button.clicked.connect(self.getProject)
#        editmode = self.dlg.findChild(QLineEdit,"opdrg")
#        editmode.setText("Editing mode in-active")
        # show the dialog
        self.dlg.opdrg.clear()
        self.dlg.button.clicked.connect(self.select_input_file)
        self.dlg.projnr.clicked.connect(self.projFolderOpen)
        self.dlg.show()

        # Run the dialog event loop
        result = self.dlg.exec_()

        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass
