# Personal Website House Sensor Data Generation

This runs on a raspberry pi and is comprised of two separate physical switches that turn on each of two individual features.

* Switch one

    * When on takes pictures and if it sees a registered face in the image then it turns on a relay which is connected to a light

* Switch two

    * When on, every 10 minutes it will read from the following sensors and add that data to an s3 bucket

        * humidity sensor
        * temperature sensor
        * light sensor 
        * sound decible sensor