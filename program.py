#!/usr/bin/python

import os
import pygtk
from facerec import face_finder
from xlwt import Workbook
pygtk.require('2.0')

import gtk

if gtk.pygtk_version < (2,3,90):
	print "PyGtk 2.3.90 or later required for this example"
	raise SystemExit

img_path = None

class Application():

	def __init__(self):
		self.window = gtk.Window()
		self.window.set_title("Face Recognizer")
		self.window.set_default_size(400, 200)
		self.window.set_position(gtk.WIN_POS_CENTER_ALWAYS)

		self.create_widgets()
		self.connect_signals()

		self.window.show_all()
		gtk.main()

	def create_widgets(self):
		self.vbox = gtk.VBox()

		self.hbox_1 = gtk.HBox()
		self.label_1 = gtk.Label("FACE RECOGNIZER")
		self.hbox_1.pack_start(self.label_1)

		self.hbox_2 = gtk.HBox()
		self.label_2 = gtk.Label("Please choose your image file for face recognition")
		self.hbox_2.pack_start(self.label_2)

		self.hbox_3 = gtk.HBox()
		self.button_filechoose = gtk.Button("Browse")
		self.hbox_3.pack_start(self.button_filechoose)

		self.hbox_4 = gtk.HBox()
		self.button_start = gtk.Button("Start Processing")
		self.hbox_4.pack_start(self.button_start)
		
		self.hbox_5 = gtk.HBox()
		self.button_exit = gtk.Button("Exit")
		self.hbox_5.pack_start(self.button_exit)

		self.vbox.pack_start(self.hbox_1)
		self.vbox.pack_start(self.hbox_2)
		self.vbox.pack_start(self.hbox_3)
		self.vbox.pack_start(self.hbox_4)
		self.vbox.pack_start(self.hbox_5)
		
		self.window.add(self.vbox)

	def connect_signals(self):
		self.button_exit.connect("clicked", self.callback_exit)
		self.button_filechoose.connect("clicked", self.callback_filechooser)
		self.button_start.connect("clicked", self.callback_start)
		self.window.connect('destroy', gtk.main_quit)

	def callback_ok(self, widget, callback_data=None):
		name = self.entry.get_text()
		print name	

	def callback_exit(self, widget, callback_data=None):
		gtk.main_quit()

	# Dialog box

	def callback_filechooser(self, widget, callback_data=None):
		dialog = gtk.FileChooserDialog("Open..", 
						None,
						gtk.FILE_CHOOSER_ACTION_OPEN,
						(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
						gtk.STOCK_OPEN, gtk.RESPONSE_OK))
		dialog.set_default_response(gtk.RESPONSE_OK)

		filter = gtk.FileFilter()
		filter.set_name("Images")
		filter.add_mime_type("image/png")
		filter.add_mime_type("image/jpeg")
		filter.add_mime_type("image/gif")
		filter.add_pattern("*.png")
		filter.add_pattern("*.jpg")
		filter.add_pattern("*.gif")
		filter.add_pattern("*.tif")
		filter.add_pattern("*.xpm")
		dialog.add_filter(filter)

		response = dialog.run()
		if response == gtk.RESPONSE_OK:
			print dialog.get_filename(), 'selected'
			global img_path
			img_path = dialog.get_filename()

			self.hbox_6 = gtk.HBox()
			self.image = gtk.Image()
			self.image.set_from_file(img_path)
			self.image.show()
			self.button_image = gtk.Button()
			self.button_image.add(self.image)
			self.button_image.show()
			self.hbox_6.pack_start(self.button_image)

			self.vbox.pack_start(self.hbox_6)

			self.window.show_all()
			dialog.destroy()
			
		elif response == gtk.RESPONSE_CANCEL:
			print 'Closed, no files selected'
		dialog.destroy()
		return img_path

	# end of Dialog box
		
	
	def callback_start(self, widget, callback_data=None):
		if img_path == None:
			message = gtk.MessageDialog(type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK)
			message.set_markup("Please choose an image file to process.")
			message.run()
			message.destroy()
		else:
			identified = face_finder(img_path)
			wb = Workbook()
			sheet1 = wb.add_sheet("Students")
			sheet1.col(0).width = 7000
			sheet1.write(0, 0, 'Following students are present:')
			row = 1
			for d in identified:
				sheet1.write(row, 0, d)
				row += 1
			wb.save('output/result.xls')
			message = gtk.MessageDialog(type=gtk.MESSAGE_INFO, buttons=gtk.BUTTONS_OK)
			message.set_markup("Show Result")
			message.run()
			message.destroy()
			os.system('xdg-open output/result.xls')
	
if __name__ == "__main__":
	app = Application()	
		
