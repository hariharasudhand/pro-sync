import React, { Component } from 'react';
import { AppRegistry, Text, View, Linking, Vibration } from 'react-native';

import { RNCamera } from 'react-native-camera';

import styles from './styles';

export default class ScanScreen extends Component {
  state = {
    isCameraReady: false,
  };
  constructor(props) {
    super(props);
    this.handleCameraReady = this.handleCameraReady.bind(this);
    this.state = {
      scanning: true,
      cameraType: RNCamera.Constants.Type.back,
    };
  }

  handleCameraReady() {
    this.setState({
      isCameraReady: true,
    });
  }

  _handleBarCodeRead(e) {
    Vibration.vibrate();
    this.setState({ scanning: false });
    Linking.openURL(e.data).catch(err =>
      console.error('An error occured', err),
    );
    return;
  }
  getInitialState() {
    return {
      scanning: true,
      cameraType: RNCamera.Constants.Type.back,
    };
  }
  render() {
    if (this.state.scanning) {
      return (
        <View style={styles.container}>
          <Text style={styles.welcome}>Focus on the Barcode or QRCode to Scan</Text>
          <View style={styles.rectangleContainer}>
            <RNCamera
              style={styles.camera}
              type={this.state.cameraType}
              flashMode={
                this.state.isCameraReady
                  ? RNCamera.Constants.FlashMode.torch
                  : RNCamera.Constants.FlashMode.off
              }
              onCameraReady={this.handleCameraReady}
              onBarCodeRead={this._handleBarCodeRead.bind(this)}
              ref={cam => (this.camera = cam)}>
              <View style={styles.rectangleContainer}>
                <View style={styles.rectangle} />
              </View>
            </RNCamera>
          </View>

        </View>
      );
    } else {
      return (
        <View style={styles.container}>
          <Text style={styles.welcome}>Barcode Scanner</Text>
          <Text style={styles.instructions}>
            Double tap R on your keyboard to reload,{'\n'}
          </Text>
        </View>
      );
    }
  }
}
AppRegistry.registerComponent('ScanScreen', () => ScanScreen);
