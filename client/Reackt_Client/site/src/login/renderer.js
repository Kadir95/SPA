import React from "react";
import "../sass/_loginSty.scss";
import { runInThisContext } from "vm";
export class Login extends React.Component {

    constructor(props){
        super(props);
        this.state = { isLoginOpen: true, isRegisterOpen: false };

    }

    showLoginBox() {
        this.setState({isRegisterOpen:false,isLoginOpen: true});
    }


    showRegisterBox() {
        this.setState({isRegisterOpen:true,isLoginOpen: false});
    }

    render() {

        return(
            <div className="root-container">
                
                <div className="box-controller">
                    <div className={"controller"+ (this.state.isLoginOpen ? " selected-controller":"")} onClick={this.showLoginBox.bind(this)}>
                        Login
                        
                    </div>
                    <div className={"controller"+ (this.state.isRegisterOpen ? " selected-controller":"")} onClick={this.showRegisterBox.bind(this)}> 
                        Register
                        
                    </div>
                </div>

                <div className="box-container">

                    {this.state.isLoginOpen && <LoginBox />}
                    {this.state.isRegisterOpen && <RegisterBox />}

                </div>

            </div>

        );

    }

}

class LoginBox extends React.Component{
    constructor(props){
        super(props);
        this.state = {};

    }

    submitLogin(e){
            //git server a git sor bakıyım ben ordamıyım?
    }

    render(){

        return(
            <div className="inner-container">
                <div className="header">
                    Login
                </div>
                <div className="box">
                    <div className="input-group">

                        <label htmlFor="username">Username</label>
                        <input type="text" name="username" className="login-input" placeholder="Username"/>

                    </div>
                    <div className="input-group">

                        <label htmlFor="password">Password</label>
                        <input type="password" name="password" className="login-input" placeholder="Password"/>

                    </div>

                    <button type="button" className="login-btn" onClick={this.submitLogin.bind(this)}>Login</button>

                </div>

            </div>
        );
        }
}


class RegisterBox extends React.Component{
    constructor(props){
        super(props);
        this.state = { 
            username: "",
            email: "",
            password: "",
            errors: [],
            pwdState: null
        };

    }

    showValidationErr(elm,msg){
        this.setState((prevState) => ({errors: [...prevState.errors, { elm, msg }] } ));
    }

    clearValidationErr(elm){
        this.setState((prevState) => {
            let newArr = [];
            for(let err of prevState.errors)
            {
                if(elm != err.elm)
                {
                    newArr.push(err);
                }
            }
            return {errors:newArr};
        });
    }

    onUsernameChange(e){
        this.setState({username: e.target.value});
        this.clearValidationErr("username");
    }

    onEmailChange(e){
        this.setState({email: e.target.value});
        this.clearValidationErr("email");
    }

    onPasswordChange(e){
        this.setState({password: e.target.value});
        this.clearValidationErr("password");


        this.setState({pwdState: "weak"});

        if(e.target.value.length >8)
        {
            this.setState({pwdState: "medium"});
        }
        if(e.target.value.length >12)
        {
            this.setState({pwdState: "strong"});
        }
    }




    submitRegister(e){
        if(this.state.username == ""){
            this.showValidationErr("username", "bu isim yerine bir şeyler yaz");
        }if(this.state.email == ""){
            this.showValidationErr("email", "bu email yerine bir şeyler yaz");
        }if(this.state.password == ""){
            this.showValidationErr("password", "bu şifre yerine bir şeyler yaz");
        }
    }

    render(){

        let usernameErr = null, passwordErr = null, emailErr = null;

        for(let err of this.state.errors)
        {
            if(err.elm == "username")
            {usernameErr = err.msg;}
            if(err.elm == "password")
            {passwordErr = err.msg;}
            if(err.elm == "email")
            {emailErr = err.msg;}
        }

        let pwdWeak = null, pwdMedium = null, pwdStrong = null;

        if(this.state.pwdState == "weak"){
            pwdWeak = true;
        } else if (this.state.pwdState == "medium"){
            pwdWeak = true;
            pwdMedium = true;
        } else if (this.state.pwdState == "strong"){
            pwdWeak = true;
            pwdMedium = true;
            pwdStrong = true;
        }

        return(
            <div className="inner-container">

                <div className="header">
                    Register
                </div>
                <div className="box">

                    <div className="input-group">

                        <label htmlFor="username">Username</label>
                        <input 
                            type="text"
                            name="username" 
                            className="login-input" 
                            placeholder="Username"
                            onChange={this.onUsernameChange.bind(this)}
                        />
                        <small className="danger-error">{ usernameErr ? usernameErr : "" }</small>
                    </div>

                    <div className="input-group">

                        <label htmlFor="email">E-mail</label>
                        <input
                            type="text"
                            name="email"
                            className="login-input"
                            placeholder="Email"
                            onChange={this.onEmailChange.bind(this)}
                        />
                        <small className="danger-error">{ emailErr ? emailErr : "" }</small>

                    </div>

                    <div className="input-group">

                        <label htmlFor="password">Password</label>
                        <input
                            type="password"
                            name="password"
                            className="login-input"
                            placeholder="Password"
                            onChange={this.onPasswordChange.bind(this)}
                        />
                        <small className="danger-error">{ passwordErr ? passwordErr : "" }</small>

                        {this.state.password && <div className="password-state">

                            <div className={"pwd pwd-weak " + (pwdWeak ? "show": "")}></div>
                            <div className={"pwd pwd-medium " + (pwdMedium ? "show": "")}></div>
                            <div className={"pwd pwd-strong " + (pwdStrong ? "show": "")}></div>

                        </div>}

                    </div>

                    <button type="button" className="login-btn" onClick={this.submitRegister.bind(this)}>Register</button>

                </div>

            </div>
        )
        

        }

}