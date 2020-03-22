import * as React from 'react';
import { Button, View } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import Icon from 'react-native-vector-icons/FontAwesome5';
import ScanOptions from './components/ScanOptions';
import SettingsScreen from './components/SettingsScreen';

import styles from './components/styles';

const Tab = createBottomTabNavigator();

// function ProfileScreen({navigation}) {
//   return (
//     <Text style={styles.welcome}>Barcode Scanner</Text>
//     <View style={styles.container}>
//       <Button
//         title="Go to Notifications"
//         onPress={() => navigation.navigate('Notifications')}
//       />
//       <Button title="Go back" onPress={() => navigation.goBack()} />
//     </View>
//   );
// }

const Stack = createStackNavigator();

function MyStack({ navigation }) {
  return (
    <Tab.Navigator
      initialRouteName="Others"
      tabBarOptions={{
        style: {
          backgroundColor: '#f2f2f2',
        },
        activeTintColor: '#a6a6a6',
      }}>
      <Tab.Screen
        name="Codes"
        component={ScanOptions}
        options={{
          tabBarLabel: 'Validate',
          tabBarIcon: ({ tintColor }) => (
            <Icon name="qrcode" type="fontawesome" size={25} color="#40bf80" bold />
          ),
          tabBarOptions: {
            activeTintColor: '#a6a6a6',
            inactiveTintColor: '#40bf80',
          },
          headerRight: () => (
            <Button onPress={() => setCount(c => c + 1)} title="Update count" />
          ),
        }}
      />
      <Tab.Screen
        name="Upload"
        component={SettingsScreen}
        options={{
          tabBarLabel: 'Settings',
          tabBarIcon: ({ tintColor }) => (
            <Icon name="user-circle" type="fontawesome" size={25} color="#40bf80" bold />
          ),
          tabBarOptions: {
            activeTintColor: '#a6a6a6',
            inactiveTintColor: '#40bf80',
          },
        }}
      />

      <Tab.Screen
        name="Others"
        component={SettingsScreen}
        options={{
          tabBarLabel: 'Others',
          tabBarIcon: ({ tintColor }) => (
            <Icon name="cubes" type="fontawesome" size={25} color="#40bf80" bold />
          ),
          tabBarOptions: {
            activeTintColor: '#a6a6a6',
            inactiveTintColor: '#40bf80',
          },
        }}
      />
    </Tab.Navigator>
  );
}

export default function App() {
  return (
    <NavigationContainer>
      <MyStack />
    </NavigationContainer>
  );
}
