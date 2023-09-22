import React from 'react';
import validator from 'validator';
import xtype from 'xtypejs';

//arrow functional component
export const Deploy = () => {


    //create state variables to store user input
    const [name, setName] = React.useState('');
    const [height, setHeight] = React.useState('');
    const [email, setEmail] = React.useState('');

    //create state variables to store VALIDITY of user input
    const [nameIsValid, setNameIsValid] = React.useState(false);
    const [heightIsValid, setHeightIsValid] = React.useState(false);
    const [emailIsValid, setEmailIsValid] = React.useState(false);

    //create state variables to error messages
    const [nameErrorMessage, setNameErrorMessage] = React.useState('');
    const [heightErrorMessage, setHeightErrorMessage] = React.useState('');
    const [emailErrorMessage, setEmailErrorMessage] = React.useState('');

    //create state variables to store submit status & submit message
    const [submittedStatus, setSubmittedStatus] = React.useState(false);

    //state variable for confirmation modal
    const [showModel, setShowModel] = React.useState(false);

    //updating function for when therer is a change in text field
    const nameChangeHandler = (e) => {
        setName(e.target.value);
        //check if name is less than 100 chacters, more than 0 and isn't a number
        if (e.target.value.trim().length > 100 || e.target.value.trim().length === 0 || xtype.type(parseInt(e.target.value)) === 'number') {
            setNameIsValid(false);
            setNameErrorMessage("You have entered an invalid name. Please enter a valid name.")
        } else {
            setNameIsValid(true);
        }
    }

    //updating function for when therer is a change in text field
    const heightChangeHandler = (e) => {
        setHeight(e.target.value);
        //check if height is a positive interger
        if (xtype.type(parseInt(e.target.value)) !== 'number' || parseInt(e.target.value) < 1) {
            setHeightIsValid(false);
            setHeightErrorMessage("You have entered an invalid height. Please enter a valid height.")
        } else {
            setHeightIsValid(true);
        }
    }

    //updating function for when therer is a change in text field
    const emailChangeHandler = (e) => {
        setEmail(e.target.value);
        //check if email has a valid format
        if (!validator.isEmail(e.target.value.trim())) {
            setEmailIsValid(false);
            setEmailErrorMessage("You have entered an invalid email. Please enter a valid email.")
        } else {
            setEmailIsValid(true);
        }
    }

    //create modal functional component to display confirmation
    function Modal({ closeModal }) {
        return (
            <div className="modal">
                <div className="modal2">
                    <p className="modalBody"> An email has been sent with your height. </p>
                    <button className="modalButton" onClick={() => {closeModal(false); setName(""); setHeight(""); setEmail("")} }
                    > Close </button>
                </div>
            </div>
        );
    }

    const submitFunc = () => {

        // if input is valid 
        if (nameIsValid === true && heightIsValid === true && emailIsValid === true) {
            //create a fetch request for the submit button
            fetch('/api', {
                method: 'POST', //request protocol
                headers: { 'Content-Type': 'application/json' }, //format of data
                body: JSON.stringify({ name, email, height }) //data being sent
            })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        setSubmittedStatus(true);
                        //open confirmation page
                        setShowModel(true)
                    } else {
                        setSubmittedStatus(false);
                        data.invalid.map((input) => {
                            if (input === 'name') {
                                setNameIsValid(false);
                            }
                            else if (input === 'height') {
                                setHeightIsValid(false);
                            }
                            else if (input === 'email') {
                                setEmailIsValid(false);
                            }
                        });
                    }
                }); //.then(response => response.json().then(data => {console.log(data)}));  
        }
    }

    return (<div className="container1">

            {/*Display submit message if input is submitted */}
            {submittedStatus === true && showModel === true ?
                <>
                    <Modal closeModal={setShowModel} />
                </>
                : null
            }

            <div className="container2">

                <header>
                    <h1 className="title">Please Enter Your Height</h1>
                </header>


                <div className="container3">
                    <p className="label">Name</p>
                    <input type="text" value={name} className='textField' placeholder="Enter your name" onChange={nameChangeHandler} />
                    {/*Display Error message if there's an error */}
                    {!nameIsValid && nameErrorMessage !== '' ?
                        <>
                            <p className="errorMessage"> {nameErrorMessage} </p>
                        </>
                        : null
                    }
                </div>

                <div className="container3">
                    <p className="label">Height (cm)</p>
                    <input type="number" value={height} className='textField' placeholder="Enter your height" onChange={heightChangeHandler} />
                    {/*Display Error message if there's an error */}
                    {!heightIsValid && heightErrorMessage !== '' ?
                        <>
                            <p className="errorMessage"> {heightErrorMessage} </p>
                        </>
                        : null
                    }
                </div>

                <div className="container3">
                    <p className="label">Email</p>
                    <input type="email" value={email} className='textField' placeholder="Enter your email" onChange={emailChangeHandler} />
                    {/*Display Error message if there's an error */}
                    {!emailIsValid && emailErrorMessage !== '' ?
                        <>
                            <p className="errorMessage"> {emailErrorMessage} </p>
                        </>
                        : null
                    }
                </div>

                <button onClick={submitFunc} className='btn'>Submit</button>

            </div>
        </div>)

}