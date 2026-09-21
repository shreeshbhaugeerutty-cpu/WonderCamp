import { useState } from 'react';
import RVexplorer from './pages/RVexplorer';
import RVDetails from './pages/RVdetails'; 

function App() {
  const [selectedRV, setSelectedRV] = useState(null);

  return (
    <div>
      {selectedRV ? (
        <RVDetails rvId={selectedRV} onBack={() => setSelectedRV(null)} />
      ) : (
        <RVexplorer onSelectRV={(rv) => setSelectedRV(rv)} />
      )}
    </div>
  );
}

export default App;