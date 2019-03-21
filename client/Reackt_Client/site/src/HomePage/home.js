import React from "react";
import "../sass/_loginSty.scss";
import { runInThisContext } from "vm";
export class Home extends React.Component {


    
    constructor(props){
        super(props);
        this.state = { isLoginOpen: true, isRegisterOpen: true };

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
                
                <div className="box-controller2">
                    <div className={"controller"+ (this.state.isLoginOpen ? " selected-controller":"")} onClick={this.showLoginBox.bind(this)}>
                        Create course
                        
                    </div>
                    <div className={"controller"+ (this.state.isRegisterOpen ? " selected-controller":"")} onClick={this.showRegisterBox.bind(this)}> 
                        Create faculty
                        
                    </div>
                    <div className={"controller"+ (this.state.isRegisterOpen ? " selected-controller":"")} onClick={this.showRegisterBox.bind(this)}> 
                        Create section
                        
                    </div>
                    <div className={"controller"+ (this.state.isRegisterOpen ? " selected-controller":"")} onClick={this.showRegisterBox.bind(this)}> 
                        Create department
                        
                    </div>
                    <div className={"controller"+ (this.state.isRegisterOpen ? " selected-controller":"")} onClick={this.showRegisterBox.bind(this)}> 
                        create student
                        
                    </div>
                    <div className={"controller"+ (this.state.isRegisterOpen ? " selected-controller":"")} onClick={this.showRegisterBox.bind(this)}> 
                        Create course
                        
                    </div>

                </div>

                <div className="box-container">

                    {this.state.isRegisterOpen && <CreateCourse />}

                </div>

            </div>

        );

    }

}




class CreateCourse extends React.Component{
    constructor(props){
        super(props);
        this.state = { 
            depID: "",
            name: "",
            courseCode: "",
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

    ondepIDChange(e){
        this.setState({depID: e.target.value});
        this.clearValidationErr("depID");
    }

    onnameChange(e){
        this.setState({name: e.target.value});
        this.clearValidationErr("name");
    }

    oncourseCodeChange(e){
        this.setState({courseCode: e.target.value});
        this.clearValidationErr("courseCode");


    }




    submitRegister(e){
        if(this.state.depID == ""){
            this.showValidationErr("depID", "bu depıd yanlış olmasın?");
        }if(this.state.name == ""){
            this.showValidationErr("name", "bu name yerine bir şeyler yaz");
        }if(this.state.courseCode == ""){
            this.showValidationErr("courseCode", "bu şifre yerine bir şeyler yaz");
        }
    }

    render(){

        let depIDErr = null, courseCodeErr = null, nameErr = null;

        for(let err of this.state.errors)
        {
            if(err.elm == "depID")
            {depIDErr = err.msg;}
            if(err.elm == "courseCode")
            {courseCodeErr = err.msg;}
            if(err.elm == "name")
            {nameErr = err.msg;}
        }

        
        return(
            <div className="inner-container">

                <div className="header">
                    Create Course
                </div>
                <div className="box">

                    <div className="input-group">

                        <label htmlFor="depID">depID</label>
                        <input 
                            type="text"
                            name="depID" 
                            className="login-input" 
                            placeholder="depID"
                            onChange={this.ondepIDChange.bind(this)}
                        />
                        <small className="danger-error">{ depIDErr ? depIDErr : "" }</small>
                    </div>

                    <div className="input-group">

                        <label htmlFor="name">Name</label>
                        <input
                            type="text"
                            name="name"
                            className="login-input"
                            placeholder="name"
                            onChange={this.onnameChange.bind(this)}
                        />
                        <small className="danger-error">{ nameErr ? nameErr : "" }</small>

                    </div>

                    <div className="input-group">

                        <label htmlFor="courseCode">Course code</label>
                        <input
                            type="text"
                            name="courseCode"
                            className="login-input"
                            placeholder="Course code"
                            onChange={this.oncourseCodeChange.bind(this)}
                        />
                        <small className="danger-error">{ courseCodeErr ? courseCodeErr : "" }</small>


                    </div>

                    <button type="button" className="login-btn" onClick={this.submitRegister.bind(this)}>Create Course</button>

                </div>

            </div>
        )
        

        }

}