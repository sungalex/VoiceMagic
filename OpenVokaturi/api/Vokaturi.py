# Vokaturi.py
# Copyright (C) 2016 Paul Boersma, Johnny Ip, Toni Gojani
# version 2018-07-27

# This file is the Python interface to the Vokaturi library.
# The declarations are parallel to those in Vokaturi.h.

import ctypes

class Quality(ctypes.Structure):
	_fields_ = [
		("valid",                ctypes.c_int),
		("num_frames_analyzed",  ctypes.c_int),
		("num_frames_lost",      ctypes.c_int)]

class EmotionProbabilities(ctypes.Structure):
	_fields_ = [
		("neutrality",  ctypes.c_double),
		("happiness",   ctypes.c_double),
		("sadness",     ctypes.c_double),
		("anger",       ctypes.c_double),
		("fear",        ctypes.c_double)]

_library = None

def load(path_to_Vokaturi_library):
	global _library

	_library = ctypes.CDLL(path_to_Vokaturi_library)

	_library.VokaturiVoice_create.restype = ctypes.c_void_p
	_library.VokaturiVoice_create.argtypes = [
		ctypes.c_double,                           # sample_rate
		ctypes.c_int]                              # buffer_length

	_library.VokaturiVoice_setRelativePriorProbabilities.restype = None
	_library.VokaturiVoice_setRelativePriorProbabilities.argtypes = [
		ctypes.c_void_p,                           # voice
		ctypes.POINTER (EmotionProbabilities)]     # priorEmotionProbabilities

	_library.VokaturiVoice_fill.restype = None     # deprecated
	_library.VokaturiVoice_fill.argtypes = [
		ctypes.c_void_p,                           # voice
		ctypes.c_int,                              # num_samples
		ctypes.POINTER (ctypes.c_double)]          # samples

	_library.VokaturiVoice_fill_float64array.restype = None
	_library.VokaturiVoice_fill_float64array.argtypes = [
		ctypes.c_void_p,                           # voice
		ctypes.c_int,                              # num_samples
		ctypes.POINTER (ctypes.c_double)]          # samples

	_library.VokaturiVoice_fill_float32array.restype = None
	_library.VokaturiVoice_fill_float32array.argtypes = [
		ctypes.c_void_p,                           # voice
		ctypes.c_int,                              # num_samples
		ctypes.POINTER (ctypes.c_float)]           # samples

	_library.VokaturiVoice_fill_int32array.restype = None
	_library.VokaturiVoice_fill_int32array.argtypes = [
		ctypes.c_void_p,                           # voice
		ctypes.c_int,                              # num_samples
		ctypes.POINTER (ctypes.c_int)]             # samples

	_library.VokaturiVoice_fill_int16array.restype = None
	_library.VokaturiVoice_fill_int16array.argtypes = [
		ctypes.c_void_p,                           # voice
		ctypes.c_int,                              # num_samples
		ctypes.POINTER (ctypes.c_short)]           # samples

	_library.VokaturiVoice_fill_float64value.restype = None
	_library.VokaturiVoice_fill_float64value.argtypes = [
		ctypes.c_void_p,                           # voice
		ctypes.c_double]                           # sample

	_library.VokaturiVoice_fill_float32value.restype = None
	_library.VokaturiVoice_fill_float32value.argtypes = [
		ctypes.c_void_p,                           # voice
		ctypes.c_float]                            # sample

	_library.VokaturiVoice_fill_int32value.restype = None
	_library.VokaturiVoice_fill_int32value.argtypes = [
		ctypes.c_void_p,                           # voice
		ctypes.c_int]                              # sample

	_library.VokaturiVoice_fill_int16value.restype = None
	_library.VokaturiVoice_fill_int16value.argtypes = [
		ctypes.c_void_p,                           # voice
		ctypes.c_int]                              # sample (yes, 32 bits, because of C argument sizes)

	_library.VokaturiVoice_fillInterlacedStereo_float64array.restype = None
	_library.VokaturiVoice_fillInterlacedStereo_float64array.argtypes = [
		ctypes.c_void_p,                           # voice left-channel
		ctypes.c_void_p,                           # voice right-channel
		ctypes.c_int,                              # num_samples_per_channel
		ctypes.POINTER (ctypes.c_double)]          # samples

	_library.VokaturiVoice_fillInterlacedStereo_float32array.restype = None
	_library.VokaturiVoice_fillInterlacedStereo_float32array.argtypes = [
		ctypes.c_void_p,                           # voice left-channel
		ctypes.c_void_p,                           # voice right-channel
		ctypes.c_int,                              # num_samples_per_channel
		ctypes.POINTER (ctypes.c_float)]           # samples

	_library.VokaturiVoice_fillInterlacedStereo_int32array.restype = None
	_library.VokaturiVoice_fillInterlacedStereo_int32array.argtypes = [
		ctypes.c_void_p,                           # voice left-channel
		ctypes.c_void_p,                           # voice right-channel
		ctypes.c_int,                              # num_samples_per_channel
		ctypes.POINTER (ctypes.c_int)]             # samples

	_library.VokaturiVoice_fillInterlacedStereo_int16array.restype = None
	_library.VokaturiVoice_fillInterlacedStereo_int16array.argtypes = [
		ctypes.c_void_p,                           # voice left-channel
		ctypes.c_void_p,                           # voice right-channel
		ctypes.c_int,                              # num_samples_per_channel
		ctypes.POINTER (ctypes.c_short)]           # samples

	_library.VokaturiVoice_extract.restype = None
	_library.VokaturiVoice_extract.argtypes = [
		ctypes.c_void_p,                           # voice
		ctypes.POINTER (Quality),                  # quality
		ctypes.POINTER (EmotionProbabilities)]     # emotionProbabilities

	_library.VokaturiVoice_reset.restype = None
	_library.VokaturiVoice_reset.argtypes = [
		ctypes.c_void_p]                           # voice

	_library.VokaturiVoice_destroy.restype = None
	_library.VokaturiVoice_destroy.argtypes = [
		ctypes.c_void_p]                           # voice

	_library.Vokaturi_versionAndLicense.restype = ctypes.c_char_p
	_library.Vokaturi_versionAndLicense.argtypes = []

class Voice:

	def __init__(self, sample_rate, buffer_length):
		self._voice = _library.VokaturiVoice_create(sample_rate, buffer_length)

	def setRelativePriorProbabilities(self, priorEmotionProbabilities):
		_library.VokaturiVoice_setRelativePriorProbabilities(self._voice, priorEmotionProbabilities)

	def fill(self, num_samples, samples): # deprecated
		_library.VokaturiVoice_fill(self._voice, num_samples, samples)

	def fill_float64array(self, num_samples, samples):
		_library.VokaturiVoice_fill_float64array(self._voice, num_samples, samples)

	def fill_float32array(self, num_samples, samples):
		_library.VokaturiVoice_fill_float32array(self._voice, num_samples, samples)

	def fill_int32array(self, num_samples, samples):
		_library.VokaturiVoice_fill_int32array(self._voice, num_samples, samples)

	def fill_int16array(self, num_samples, samples):
		_library.VokaturiVoice_fill_int16array(self._voice, num_samples, samples)

	def fill_float64value(self, sample):
		_library.VokaturiVoice_fill_float64value(self._voice, sample)

	def fill_float32value(self, sample):
		_library.VokaturiVoice_fill_float32value(self._voice, sample)

	def fill_int32value(self, sample):
		_library.VokaturiVoice_fill_int32value(self._voice, sample)

	def fill_int16value(self, sample):
		_library.VokaturiVoice_fill_int16value(self._voice, sample)

	def extract(self, quality, emotionProbabilities):
		_library.VokaturiVoice_extract(self._voice, quality, emotionProbabilities)

	def reset(self):
		_library.VokaturiVoice_reset(self._voice)

	def destroy(self):
		if not _library is None:
			_library.VokaturiVoice_destroy(self._voice)

def Voices_fillInterlacedStereo_float64array(left, right, num_samples_per_channel, samples):
	_library.VokaturiVoice_fillInterlacedStereo_float64array(left._voice, right._voice, num_samples_per_channel, samples)

def Voices_fillInterlacedStereo_float32array(left, right, num_samples_per_channel, samples):
	_library.VokaturiVoice_fillInterlacedStereo_float32array(left._voice, right._voice, num_samples_per_channel, samples)

def Voices_fillInterlacedStereo_int32array(left, right, num_samples_per_channel, samples):
	_library.VokaturiVoice_fillInterlacedStereo_int32array(left._voice, right._voice, num_samples_per_channel, samples)

def Voices_fillInterlacedStereo_int16array(left, right, num_samples_per_channel, samples):
	_library.VokaturiVoice_fillInterlacedStereo_int16array(left._voice, right._voice, num_samples_per_channel, samples)

def versionAndLicense():
	return _library.Vokaturi_versionAndLicense().decode("UTF-8")

def SampleArrayC(size): # deprecated
	return (ctypes.c_double * size)()

def SampleArrayCdouble(size):
	return (ctypes.c_double * size)()

def SampleArrayCfloat(size):
	return (ctypes.c_float * size)()

def SampleArrayCint(size):
	return (ctypes.c_int * size)()

def SampleArrayCshort(size):
	return (ctypes.c_short * size)()
