#pragma once

/* RC18-B2.1 frozen simulation candidate -- 2026-09-23
 *
 * H(z) = (b0 + b1 z^-1 + b2 z^-2) / (1 + a1 z^-1 + a2 z^-2)
 * Fs = 2.000 MHz
 *
 * IMPORTANT: these coefficients passed the repository's numerical model.
 * They do not by themselves prove a measured MCU latency/jitter budget.
 */

#define RC18_CONTROL_FS_HZ       2000000.0f
#define RC18_TOTAL_DELAY_TARGET_S 2.041e-6f
#define RC18_JITTER_BOUND_S       25.0e-9f

static const float rc18_biquad_b0 =  1.960055470f;
static const float rc18_biquad_b1 = -2.818402052f;
static const float rc18_biquad_b2 =  0.925601721f;
static const float rc18_biquad_a1 = -1.029690862f;
static const float rc18_biquad_a2 =  0.096946053f;

/* CMSIS-DSP Q31 DF1 model used by validation. Feedback signs are reversed
 * relative to the denominator form above. postShift = 2.
 */
#define RC18_Q31_POSTSHIFT 2
static const int rc18_biquad_q31[5] = {
     1052296778,
    -1513118047,
      496928640,
      552811055,
      -52047514
};
