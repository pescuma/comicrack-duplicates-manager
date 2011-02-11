#####################################################################################################
##
##      BookWrapper.py - part of duplicatemanager, a script for comicrack
##
##      Author: Pescuma Domenecci , modified by perezmu
##
##      Orignally from pescumas' series info panel script. 
##
######################################################################################################


### original credits
"""
Copyright (C) 2010 Ricardo Pescuma Domenecci

This is free software; you can redistribute it and/or
modify it under the terms of the GNU Library General Public
License as published by the Free Software Foundation; either
version 2 of the License, or (at your option) any later version.

This is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Library General Public License for more details.

You should have received a copy of the GNU Library General Public
License along with this file; see the file license.txt.  If
not, write to the Free Software Foundation, Inc., 59 Temple Place - Suite 330,
Boston, MA 02111-1307, USA.
"""
##########

"""
Modified by apm
"""

import clr
clr.AddReference('System.Drawing')
import sys
import System
from getcvdb import extract_issue_ref




class dmBookWrapper:
	_emptyVals = { 
		'Count' : '-1', 
		'Year' : '-1', 
		'Month' : '-1', 
		'AlternateCount' : '-1', 
		'Rating' : '0.0',
		'CommunityRating' : '0.0'
		}
	_dontConvert = set([ 
		'Pages',
		'PageCount',
		'FrontCoverPageIndex',
		'FirstNonCoverPageIndex',
		'LastPageRead',
		'ReadPercentage',
		'OpenedCount'
		])
	
	def __init__(self, book):
		self.raw = book
		self._pages = {}
	
	def __dir__(self):
		ret = set()
		ret.update(set(self.__dict__))
		ret.update(dir(self.raw))
		ret.update(self._getterFields)
		return list(ret)
	
	def _safeget(self, name):
		try:
			return self._get(name)
		except:
			return ''
	
	def _get(self, name):
		return ToString(getattr(self.raw, name)).strip()
	
	def __getattr__(self, name):
		if name in self._dontConvert:
			return getattr(self.raw, name)
		
		if name in self._emptyVals:
			emptVal = self._emptyVals[name]
		else:
			emptVal = ''
		
		ret = self._get(name)
		if ret == '' or ret == emptVal:
			ret = self._safeget('Shadow' + name)
		if ret == '' or ret == emptVal:
			ret = ''
		return ret
	
	def GetCover(self, width = 0, height = 0):
		coverIndex = 0 
		if self.raw.FrontCoverPageIndex > 0:
			coverIndex = self.raw.FrontCoverPageIndex
		return self.GetPage(coverIndex, width, height)
	
	def GetPage(self, page, width = 0, height = 0):
		global _oldTmpFiles, _ComicRack
		
		if not self.raw.FilePath:
			if page > 0:
				return ''
		elif page >= self.raw.PageCount:
			return ''
		
		hash = str(page) + '_' + str(width) + '_' + str(height)
		
		if hash in self._pages:
			return self._pages[hash]
		
		self._pages[hash] = ''
		
		#image = _ComicRack.App.GetComicPage(self.raw, page)
		image = _ComicRack.App.GetComicThumbnail(self.raw, page)
		if image is None:
			return ''

		tmpFile = System.IO.Path.GetTempFileName()
		_oldTmpFiles.append(tmpFile)

		# We need a jpg
		imageFile = tmpFile + '.jpg'
		_oldTmpFiles.append(imageFile)
		#print imageFile
		
		try:
			if width > 0 or height > 0:
				image = ResizeImage(image, width, height)
			
			image.Save(imageFile, System.Drawing.Imaging.ImageFormat.Jpeg)
			
			self._pages[hash] = imageFile
			
			return imageFile
			
		except Exception,e:
			print '[SeriesInfoPanel] Exception when saving image: ', e
			return ''
	
	def GetSeries(self):
		ret = self.raw.Series
		if ret:
			return ret
		ret = self.raw.ShadowSeries
		if ret:
			return ret
		return ''
	
	def GetVolume(self):
		ret = self.raw.Volume
		if ret != -1:
			return str(ret)
		ret = self.raw.ShadowVolume
		if ret != -1:
			return str(ret)
		return ''
	
	def GetNumber(self):
		ret = self.raw.Number
		if ret:
			return ret
		ret = self.raw.ShadowNumber
		if ret:
			return ret
		return ''
	
	def GetFormat(self):
		ret = self.raw.Format
		if ret:
			return ret
		ret = self.raw.ShadowFormat
		if ret:
			return ret
		return 'Series'

	def GetFileFormat(self):
		if not self.raw.FilePath:
			return 'Fileless'
		ret = self.raw.FileFormat
		if ret:
			return ret
		return self.raw.ShadowFileFormat
		if ret:
			return ret
		return Translate('Unknown')

	def GetFilePath(self):
		if not self.raw.FilePath:
			return 'Fileless'
		ret = self.raw.FilePath
		return ret

	def GetFileName(self):
		if not self.raw.FileNameWithExtension:
			return 'Fileless'
		ret = self.raw.FileNameWithExtension
		return ret


# these were added by apm


	def GetId(self):
		return self.raw.Id
	
	def GetPageCount(self):
		return self.raw.PageCount

	def GetFileSize(self):
		return self.raw.FileSize

	def GetCVDB_ID(self):
		return extract_issue_ref(self.raw)


	# Properties
	
	Cover = property(GetCover)
	Series = property(GetSeries)
	Volume = property(GetVolume)
	Number = property(GetNumber)
	Format = property(GetFormat)
	FileFormat = property(GetFileFormat)
	ID = property (GetId)
	PageCount = property(GetPageCount)
	FilePath = property(GetFilePath)
	FileName = property(GetFileName)

	FileSize = property(GetFileSize)
	CVDB_ID = property(GetCVDB_ID)


