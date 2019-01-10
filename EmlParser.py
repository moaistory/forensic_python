import glob
import datetime
import json
import eml_parser
import email
import os
import base64
import filetype
EmlDir = ".\\Storage\\*.eml"
AttachDir = ".\\Attachment"

class AttachMent() :
	def __init__(self) :
		self.path = None
		self.filename = None
		self.size = None
		self.sha256 = None
		self.md5 = None
		self.extension = None
		self.raw = None
		self.content_header = None
		self.type = None
		self.mime_type = None
		
	def parse(self, info) :
		self.filename = info['filename']
		self.size = info['size']
		self.sha256 = info['hash']['sha256']
		self.md5 = info['hash']['sha256']
		if 'extension' in info.keys() :
			self.extension = info['extension']
		self.raw = info['raw']
		self.content_header = info['content_header']
	
	def save(self, path) :
		self.path = path + "\\" + self.sha256
		if os.path.exists(self.path) :
			return
		with open(self.path, 'wb') as f_out:
			f_out.write(base64.b64decode(self.raw))
		kind = filetype.guess(self.path)
		if not kind is None:
			self.type = kind.extension
			self.mime_type = kind.mime

class EmlInfo() : 
	def __init__(self) :
		self.path = None
		self.sha256 = None
		self.md5 = None
		self.subject = None
		self.date = None
		self.from_ = None
		self.to = None
		self.return_path = None
		self.reply_to = None
		self.message_id = None
		self.attachmentList = []
	
	def parse(self, path) : 
		self.path = path
		with open(path, 'rb') as f_eml:
			raw_eml = f_eml.read()
			hash = eml_parser.eml_parser.get_file_hash(raw_eml)
			self.sha256 = hash['sha256']
			self.md5 = hash['md5']
			eml = eml_parser.eml_parser.decode_email_b(raw_eml, include_attachment_data=True)
			self.subject = eml['header']['subject']
			self.date = eml['header']['date']
			self.to = eml['header']['to']
			self.from_ = eml['header']['from']
			self.return_path = eml['header']['header']['return-path']
			
			if 'message-id' in eml['header']['header'].keys() :
				self.message_id = eml['header']['header']['message-id']
			
			if 'reply-to' in eml['header']['header'].keys() :
				self.reply_to = eml['header']['header']['reply-to']
			
			if 'attachment' in eml.keys() :
				for attachInfo in eml['attachment'] :
					attachment = AttachMent()
					attachment.parse(attachInfo)
					self.attachmentList.append(attachment)
	
	def saveAttachment(self, path) : 
		for attachment in self.attachmentList : 
			attachment.save(path)

class EmlParser() :
	def __init__(self) :
		self.path = None
		self.emlList = []
	
	def parseEml(self, emlDir, attachDir) : 
		emlPathList = glob.glob(emlDir)
		for emlPath in emlPathList :
			eml = EmlInfo()
			eml.parse(emlPath)
			eml.saveAttachment(attachDir)
			self.emlList.append(eml)
			break

if __name__ == '__main__':
	emlParser = EmlParser()
	emlParser.parseEml(EmlDir, AttachDir)

