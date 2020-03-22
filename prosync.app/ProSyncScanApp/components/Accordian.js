import React, {Component} from 'react';
import {View, TouchableOpacity, Text, FlatList} from 'react-native';
import Colors from './Colors';
import styles from './styles';
import Icon from 'react-native-vector-icons/FontAwesome5';

export default class Accordian extends Component {
  constructor(props) {
    super(props);
    this.state = {
      data: props.data,
      expanded: false,
    };
  }

  render() {
    return (
      <View>
        <TouchableOpacity
          style={styles.row}
          onPress={() => this.toggleExpand()}>
          <Text style={[styles.title, styles.font]}>{this.props.title}</Text>
          <Icon
            name={
              this.state.expanded ? 'keyboard-arrow-up' : 'keyboard-arrow-down'
            }
            size={30}
            color={Colors.DARKGRAY}
          />
        </TouchableOpacity>
        <View style={styles.parentHr} />
        {this.state.expanded && (
          <View style={{}}>
            <FlatList
              data={this.state.data}
              numColumns={1}
              scrollEnabled={false}
              renderItem={({item, index}) => (
                <View>
                  <TouchableOpacity
                    style={[
                      styles.childRow,
                      styles.button,
                      item.value ? styles.btnInActive : styles.btnActive,
                    ]}
                    onPress={() => this.onClick(index)}>
                    <Text style={[styles.font, styles.itemInActive]}>
                      {item.key}
                    </Text>
                    <Icon
                      name={'check-circle'}
                      size={24}
                      color={item.value ? Colors.LIGHTGRAY : Colors.GREEN}
                    />
                  </TouchableOpacity>
                  <View style={styles.childHr} />
                </View>
              )}
            />
          </View>
        )}
      </View>
    );
  }

  onClick = index => {
    const temp = this.state.data.slice();
    temp[index].value = !temp[index].value;
    this.setState({data: temp});
  };

  toggleExpand = () => {
    this.setState({expanded: !this.state.expanded});
  };
}
