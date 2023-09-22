import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';

//Allow for items to be rendered render(what,where)
ReactDOM.render(
  /*React's StrictMode is sort of a helper component that will:
  * Verify that the components inside are following some of the recommended practices and warn you if not in the console.
  * Verify the deprecated methods are not being used, and if they're used strict mode will warn you in the console.
  * Help you prevent some side effects by identifying potential risks.
  */
  <React.StrictMode>
    <App />  {/*create an instance of the app to be rendered */}
  </React.StrictMode>,
  document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
