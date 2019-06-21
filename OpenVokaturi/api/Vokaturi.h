#ifndef _Vokaturi_h_
#define _Vokaturi_h_
/*
 * Vokaturi.h
 *
 * Copyright (C) 2016-2019 Paul Boersma, Johnny Ip, Toni Gojani
 * version 3.3, 2019-05-30
 *
 * This code is part of OpenVokaturi and VokaturiPlus.
 *
 * OpenVokaturi is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3 of the License, or (at
 * your option) any later version.
 *
 * OpenVokaturi is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
 * See the GNU General Public License for more details.
 *
 * If you use this file with OpenVokaturi,
 * you should have received a copy of the GNU General Public License
 * along with this software. If not, see http://www.gnu.org/licenses/.
 */

#ifdef __cplusplus
	extern "C" {
#endif

typedef struct structVokaturiVoice *VokaturiVoice;

VokaturiVoice VokaturiVoice_create (
	double sample_rate,
	int buffer_length
);

typedef struct {
	double neutrality;
	double happiness;
	double sadness;
	double anger;
	double fear;
} VokaturiEmotionProbabilities;

void VokaturiVoice_setRelativePriorProbabilities (
	VokaturiVoice voice,
	VokaturiEmotionProbabilities *priorEmotionProbabilities
);

void VokaturiVoice_fill (VokaturiVoice voice, int num_samples, double samples []);
	// deprecated; identical to VokaturiVoice_fill_float64array

void VokaturiVoice_fill_float64array (VokaturiVoice voice, int num_samples, double samples []);
void VokaturiVoice_fill_float32array (VokaturiVoice voice, int num_samples, float samples []);
void VokaturiVoice_fill_int32array (VokaturiVoice voice, int num_samples, int samples []);
void VokaturiVoice_fill_int16array (VokaturiVoice voice, int num_samples, short samples []);

void VokaturiVoice_fill_float64value (VokaturiVoice voice, double sample);
void VokaturiVoice_fill_float32value (VokaturiVoice voice, float sample);
void VokaturiVoice_fill_int32value (VokaturiVoice voice, int sample);
void VokaturiVoice_fill_int16value (VokaturiVoice voice, int sample);   // NOT short, because of C argument sizes

void VokaturiVoice_fillInterlacedStereo_float64array (VokaturiVoice left, VokaturiVoice right,
	int num_samples_per_channel, double samples []);
void VokaturiVoice_fillInterlacedStereo_float32array (VokaturiVoice left, VokaturiVoice right,
	int num_samples_per_channel, float samples []);
void VokaturiVoice_fillInterlacedStereo_int32array (VokaturiVoice left, VokaturiVoice right,
	int num_samples_per_channel, int samples []);
void VokaturiVoice_fillInterlacedStereo_int16array (VokaturiVoice left, VokaturiVoice right,
	int num_samples_per_channel, short samples []);

typedef struct {
	int valid;   // 1 = "there were voiced frames, so that the measurements are valid"; 0 = "no voiced frames found"
	int num_frames_analyzed;
	int num_frames_lost;
} VokaturiQuality;

void VokaturiVoice_extract (
	VokaturiVoice voice,
	VokaturiQuality *quality,
	VokaturiEmotionProbabilities *emotionProbabilities
);

void VokaturiVoice_destroy (VokaturiVoice voice);

void VokaturiVoice_reset (VokaturiVoice voice);

const char *Vokaturi_versionAndLicense ();

#ifdef __cplusplus
	}
#endif

/* End of file Vokaturi.h */
#endif
