import './App.css';
import { useState, useEffect } from 'react';
import { addAnimalAction, adoptAnimalAction, getAnimalsAction, releaseAnimalActiono } from './utils/marketplace';
import { indexerClient, myAlgoConnect } from "./utils/constants";
import { stringToMicroAlgos } from './utils/conversions';
import Cover from "./Cover";



function App() {


  const [address, setAddress] = useState(null);
  const [name, setName] = useState("");
  const [amount, setAmount] = useState(0);
  const [description, setDescription] = useState("");
  const [image, setImage] = useState("");
  const [balance, setBalance] = useState(0);
  const [animals, setAnimals] = useState([])

  const fetchBalance = async (accountAddress) => {
    indexerClient.lookupAccountByID(accountAddress).do()
      .then(response => {
        const _balance = response.account.amount;
        setBalance(_balance);
      })
      .catch(error => {
        console.log(error);
      });
  };

  const connectWallet = async () => {
    myAlgoConnect.connect()
      .then(accounts => {
        const _account = accounts[0];
        console.log(_account)
        setAddress(_account.address);
        fetchBalance(_account.address);
        if (_account.address) getAnimals(_account.address);
      }).catch(error => {
        console.log('Could not connect to MyAlgo wallet');
        console.error(error);
      })
  };


  const adoptAnimal = (animal) => {
    adoptAnimalAction(address, animal)
      .then(() => {
        getAnimals(address);
        fetchBalance(address);
      })
      .catch(error => {
        console.log(error)
        alert(error)
      })
  }


  const releaseAnimal = (car) => {
    releaseAnimalActiono(address, car)
      .then(() => {
        getAnimals(address);
        fetchBalance(address);
      })
      .catch(error => {
        console.log(error)
        alert(error)
      })
  }


  const addAnimals = async (data) => {
    console.log(data);
    addAnimalAction(address, data)
      .then(() => {
        getAnimals(address);
        fetchBalance(address);
      })
      .catch(error => {
        console.log(error);
        alert(error)
      })
  }

  const getAnimals = async (_address) => {
    try {
      alert("fetching animals")
      const animals = await getAnimalsAction();
      setAnimals(animals);
    } catch (error) {
      alert(error)
      console.log(error);
    } finally{
      alert("fetched")
    }

  };


  const formSubmit = async (e) => {
    e.preventDefault();
    try {
      if (!name || !amount || !description || !image) return;
      await addAnimals({ name, description, amount, image} );
      getAnimals();
    } catch (error) {
      console.log(error);
    }
  };
  return (
    <>
      {address ? <div>
        <header className="site-header sticky-top py-1">
          <nav className="container d-flex flex-column flex-md-row justify-content-between">
            <a className="py-2" href="#" aria-label="Product">
              <h3>Animal Kingdom</h3>
            </a>
            <a className="py-2 d-none d-md-inline-block" href="#">
              Balance: {balance / 10 ** 6} ALGO
            </a>
          </nav>
        </header>
        <main>
          <div className="row row-cols-1 row-cols-md-3 mb-3 text-center">
            {animals.map(animal => <div className="col">
              <div className="card mb-4 rounded-3 shadow-sm">
                <div className="card-header py-3">
                  <h4 className="my-0 fw-normal">{animal.name}</h4>
                </div>
                <div className="card-body">
                  <h1 className="card-title pricing-card-title">{animal.amount / 10 ** 6}<small className="text-muted fw-light">ALGO</small></h1>
                  <img width={200} src={animal.image} alt="" />
                  <p className="list-unstyled mt-3 mb-4">
                    {animal.description}
                  </p>
                  {animal.adopted === 0 ? <button type="button"
                    onClick={() => adoptAnimal(animal)}
                    className="w-100 btn btn-lg btn-outline-primary">Adopt Animal</button>
                    : animal.owner === address ?
                      <button type="button"
                        onClick={() => releaseAnimal(animal)}
                        className="w-100 btn btn-lg btn-outline-danger">Release Animal</button>
                      : "Not the owner"}
                </div>
              </div>
            </div>)}
          </div>
        </main>


        <div className="p-3 w-50 justify-content-center">
          <h2>Add your Animal to be Adopted</h2>
          <div className="">
            <form onSubmit={formSubmit}>
              <div className="form-floating mb-3">
                <input
                  type="text"
                  className="form-control rounded-4"
                  id="floatingInput"
                  placeholder="Name"
                  onChange={(e) => setName(e.target.value)}
                  required
                />
                <label htmlFor="floatingInput">Name</label>
              </div>
              <div className="form-floating mb-3">
                <input
                  type="text"
                  className="form-control rounded-4"
                  id="floatingInput"
                  placeholder="Amount"
                  onChange={(e) => setAmount(stringToMicroAlgos(e.target.value))}
                  required
                />
                <label htmlFor="floatingInput">Amount</label>
              </div>
              <div className="form-floating mb-3">
                <input
                  className="form-control rounded-4"
                  id="floatingInput"
                  placeholder="Description"
                  onChange={(e) => setDescription(e.target.value)}
                  required
                />
                <label htmlFor="floatingInput">Description</label>
              </div>
              <div className="form-floating mb-3">
                <input
                  className="form-control rounded-4"
                  id="floatingInput"
                  placeholder="Image Url"
                  onChange={(e) => setImage(e.target.value)}
                  required
                />
                <label htmlFor="floatingInput">Image</label>
              </div>

              <button
                className="w-100 mb-2 btn btn-lg rounded-4 btn-primary"
                type="submit"
              >
                Add Your Animal
              </button>
            </form>
          </div>
        </div>
      </div> :
        <Cover name={"Animal Hub"} coverImg={"https://images.unsplash.com/photo-1629812456605-4a044aa38fbc?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=387&q=80"} connect={connectWallet} />
      }
    </>
  );
}

export default App;
