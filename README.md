<center>

![](tau_eee_logo.jpg)

</center>

# The School of Electrical Engineering  בי"ס להנדסת חשמל            


# Project: Data Analysis of Low Sampling NILM Detection

## Fields of research:

    Energy Conversion, Power Electronics, Signal Processing, Simulation & Software Development.

## Materials for the project development: 

    Python (3.8), the following libraries were also used in accordance:


@import "requirements.txt"

to install them use the following command:

```bash
pip install -r requirements.txt
```

## Initial background information:

- https://www.youtube.com/watch?v=pfSnGGunTAo&t=871s
- https://nilmtk.github.io/
- http://www.nilm.eu/

# Extraction features , Event Detection Updates

## Extraction features:
    Under development, best features still being tested.

## Concept:
    Apply energy conversion and power electronics commun formulas aligned with statistical manipulation to handle noise, filter a better SNR, distinct nominal and proportional units of change and generate frequency domain analysis and other key angles for digital signal processing.

## Things to add:
    Determine exactly which relevant features should be calculated and displayed, such as active/reactive power

## Questions:

    Where do we get the measurment instrument physical data?

    Is there a documentation for the raw data parameters? The data in InstrumParams seems to have some valuable information.

    Is there a documentation for the generated parameters in the device for the extracted data tables?
## Event detection:
    A primary draft. Yet to confirm it works. Algorithm in development stage.

## Concept:
    Apply Savgol_filter to smooth the results of the data_frame and then create a "window" of 5 samples that iterates over the extracted data frame and confirms that a pulse higher than a threshold (power=250W) leads to a new event and not a noise spike (moving average algo).
    1. Apply Savgol_filter
    2. Create a window of 5 samples
    3. Iterate the window over the extracted data
    4. If a sample is above the threshold, confirm the following sample is also above the threshold (250W)
        • If yes, new event has begun
        • If no, this sample is noise. Replace the value by taking the median of the previous sample value and the following sample value 

## Things to add:
    • Add THD to the algorithm to improve accuracy.
    • More information to the dictionary including time of sample etc…(total time of each event)
## Questions:
    • More ideas of how to apply event detection
    • Smoothed noise using savgol_filter. Any better options?
    • What is a reasonable threshold value?
    • What factors to be considered (power, THD, maybe reactive vs active power…)