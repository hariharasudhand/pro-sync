import React from 'react'
import { Icon } from 'react-native-elements'
import AppColors from './AppColors'

const Chevron = () => (
    <Icon
        name="chevron-right"
        type="entypo"
        color={AppColors.lightGray2}
        containerStyle={{ marginLeft: -15, width: 20 }}
    />
)

export default Chevron