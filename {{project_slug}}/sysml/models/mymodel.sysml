package MyModel {
    public import SI::*;

    port def PowerPort;
    port def ImagePort;

    part def Lens {
        attribute focalLength : Real = 35 [mm];
    }

    part def Sensor {
        attribute pixelCount : Integer = 24000000;

        port powerPort : PowerPort;
        port imagePort : ImagePort;
    }

    part def Camera {
        attribute mass : Real = 500 [g];
        attribute resolution : Integer = 12;

        part lens : Lens;
        part sensor : Sensor;

        port powerPort : PowerPort;
        port imagePort : ImagePort;

        connection powerConnection from powerPort to sensor.powerPort;
        connection imageConnection from sensor.imagePort to imagePort;
    }

    requirement def CameraRequirement {
        doc /* The camera shall meet performance requirements. */

        constraint massConstraint { mass <= 600 [g] }
        constraint resolutionConstraint { resolution >= 10 }
    }

    action def Focus {
        out focusedDistance : Real;
    }

    action def Expose {
        in focusDistance : Real;
        out lightValue : Real;
    }

    action def Capture {
        in exposureValue : Real;
    }

    action def TakePicture {
        in exposureSetting : Real;

        action focus : Focus;
        action expose : Expose;
        action capture : Capture;

        flow focus.focusedDistance to expose.focusDistance;
        flow expose.lightValue to capture.exposureValue;
    }
}
