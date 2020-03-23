import React, { Component } from 'react';
import { Text, View, Image } from 'react-native';
import { Button } from 'react-native-elements';

import ImagePicker from "react-native-image-picker";
import Icon from 'react-native-vector-icons/FontAwesome5';
import styles from "./styles";

class CodeUploadScreen extends Component {

  constructor(props) {
    super(props);
    this.state = {
      filePath: {},
    };
  }
  chooseFile = () => {
    var options = {
      title: 'Select Image',
      customButtons: [
        { name: 'customOptionKey', title: 'Choose Photo from Custom Option' },
      ],
      storageOptions: {
        skipBackup: true,
        path: 'images',
      },
    };
    ImagePicker.showImagePicker(options, response => {
      console.log('Response = ', response);

      if (response.didCancel) {
        console.log('User cancelled image picker');
      } else if (response.error) {
        console.log('ImagePicker Error: ', response.error);
      } else if (response.customButton) {
        console.log('User tapped custom button: ', response.customButton);
        alert(response.customButton);
      } else {
        let source = response;
        // You can also display the image using data:
        // let source = { uri: 'data:image/jpeg;base64,' + response.data };
        this.setState({
          filePath: source,
        });
      }
    });
  };

  render() {
    const { navigation } = this.props;
    return (
      <View>
        <Button style={styles.button}
          icon={
            <Icon
              name="clone"
              size={25}
              color="#e6e6e6"
            />
          }
          onPress={this.chooseFile.bind(this)}
          title="Select"
        />


        {/*<Image 
          source={{ uri: this.state.filePath.path}} 
          style={{width: 100, height: 100}} />*/}

        <Image
          source={{ uri: this.state.filePath.uri }}
          style={{ width: 350, height: 350 }}
        />
        <Button style={styles.button}
          icon={
            <Icon
              name="telegram"
              size={25}
              color="#e6e6e6"
            />
          }
          backgroundColor='#999999'
          title=" Process "
        />

        <Text style={{ alignItems: 'center' }}>
          {this.state.filePath.uri}
        </Text>


      </View>
    );
  }
}

export default CodeUploadScreen;
