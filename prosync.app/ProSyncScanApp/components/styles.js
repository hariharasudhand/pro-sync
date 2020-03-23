import { StyleSheet, Dimensions } from 'react-native';
import Colors from './Colors';

const styles = StyleSheet.create({
    container: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
        backgroundColor: '#ffffff',
    },
    camera: {
        flex: 0,
        alignItems: 'center',
        justifyContent: 'center',
        backgroundColor: 'transparent',
        height: Dimensions.get('window').width,
        width: Dimensions.get('window').width,
    },
    welcome: {
        fontSize: 20,
        textAlign: 'center',
        margin: 10,
    },
    instructions: {
        textAlign: 'center',
        color: '#333333',
        marginBottom: 5,
    },
    rectangleContainer: {
        flex: 1,
        alignItems: 'center',
        justifyContent: 'center',
        backgroundColor: 'transparent',
    },

    rectangle: {
        height: 450,
        width: 450,
        borderWidth: 2,
        borderColor: '#40bf80',
        backgroundColor: 'transparent',
    },
    title: {
        fontSize: 14,
        fontWeight: 'bold',
        color: Colors.DARKGRAY,
    },
    row: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        height: 56,
        paddingLeft: 25,
        paddingRight: 18,
        alignItems: 'center',
        backgroundColor: Colors.CGRAY,
    },
    parentHr: {
        height: 1,
        color: Colors.WHITE,
        width: '100%',
    },
    child: {
        backgroundColor: Colors.LIGHTGRAY,
        padding: 16,
    },

    accordian_container: {
        flex: 1,
        paddingTop: 100,
        backgroundColor: Colors.PRIMARY,
    },
    modal: {
        justifyContent: 'center',
        alignItems: 'center',
        backgroundColor: "#ffffff",
        height: 300,
        width: '80%',
        borderRadius: 10,
        borderWidth: 1,
        borderColor: '#40bf80',
        marginTop: 80,
        marginLeft: 40,

    },
    button: {
        marginRight: 40,
        marginLeft: 40,
        marginTop: 10,
        paddingTop: 10,
        paddingBottom: 10,
        backgroundColor: '#999999',
        borderRadius: 10,
        borderWidth: 1,
        borderColor: '#fff'

    }

});

export default styles;
