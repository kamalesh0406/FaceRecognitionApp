import React, { Component } from 'react';
import { Platform, StyleSheet, Text, View, TouchableOpacity } from 'react-native';
import * as Permissions from "expo-permissions";
import { Camera } from 'expo-camera';
import { nullLiteral } from '@babel/types';


const instructions = Platform.select({
  ios: 'Press Cmd+R to reload,\n' + 'Cmd+D or shake for dev menu',
  android: 'Double tap R on your keyboard to reload,\n' + 'Shake or press menu button for dev menu',
});

export default class CameraType extends Component{
  state = {
    hasCameraPermission: null,
    type: Camera.Constants.Type.back
  }

  async componentDidMount(){
    const { status } = await Permissions.askAsync(Permissions.CAMERA);
    this.setState({hasCameraPermission: state === "granted"});
  }

  render(){
    const { hasCameraPermission } = this.state;
    if (hasCameraPermission === null){
      <View />
    }else if (hasCameraPermission === false){
      return <Text>No access to camera</Text>
    }else{
      return (
        <View style={{flex:1}}>
          <Camera style={{flex:1}} type={this.state.type}>
            <View
              style={{
                flex:1,
                backgroundColor: 'transparent',
                flexDirection: 'row'
              }}
            >
              <TouchableOpacity
              style={{
                flex:0.1,
                alignSelf:'flex-end',
                alignItems:'center'
              }}
              onPress={() => {
                this.setState({
                  type:
                    this.state.type === Camera.Constants.Type.Back
                    ? Camera.Constants.Type.front
                    : Camera.Constants.Type.back
                });
              }}
              >
                <Text style={{ fontSize: 18, marginBottom: 10, color: 'white' }}> Flip </Text>
              </TouchableOpacity>
            </View>
          </Camera>
        </View>
      )
    }
  }
}

// const styles = StyleSheet.create({
//   container: {
//     flex: 1,
//     justifyContent: 'center',
//     alignItems: 'center',
//     backgroundColor: '#F5FCFF',
//   },
//   welcome: {
//     fontSize: 20,
//     textAlign: 'center',
//     margin: 10,
//   },
//   instructions: {
//     textAlign: 'center',
//     color: '#333333',
//     marginBottom: 5,
//   },
// });
