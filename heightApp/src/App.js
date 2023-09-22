import './App.css';
import{Deploy} from './Component/Deploy/Deploy'

//create functional component of App
function App() {
  return (
    <div className="Container">
      <Deploy/> {/*create an instance of all components (deploy component)*/}
    </div>
  );
}

export default App; //allow functional component to be exported to other files (index.js)
