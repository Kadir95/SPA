import React, { Component } from 'react';
import {Login} from './login/renderer';
import {Home} from './HomePage/home';

class App extends Component {
 
  constructor(props){
    super(props);
    this.state = {  isLoginOpen: false, isHomeopen: true  };

    }

    render() {

    return (
      <div>
        Burası login ekranı
        <hr />

                    {this.state.isLoginOpen && <Login />}
                    {this.state.isHomeopen && <Home />}

        <hr />
        bu yazı burada

      </div>
      
      )


    }

}

export default App;
