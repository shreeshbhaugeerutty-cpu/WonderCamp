
 function Header() {
  return (
    <nav>
  <div className="flex justify-evenly">
    <p className="text-4xl font-bold">Wonder Camp</p>

  <div className="relative w-full max-w-sm mx-4">
   <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-[#5B8246]">  
   <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
        <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
      </svg>
   </div>  
    <input
      type="text"
      placeholder="Search"
      class="w-545px rounded-xl border border-[#366823] bg-transparent py-1.5 pl-10 pr-4 text-sm text-[#366823] placeholder-[#80a26d] focus:outline-none"
    />
  </div>

<button >
      <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
        <path stroke-linecap="round" stroke-linejoin="round" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" />
      </svg>
    </button>

    <button>
      <div className="w-5 h-5 bg-[#326126] rounded-md relative">
        <span className="absolute -top-1 -right-1 w-2.5 h-2.5 bg-[#8BA878] rounded-full border border-[#FDFBF0]"></span>
      </div>
    </button>

    <button>
      <svg xmlns="http://www.w3.org/2000/svg" className="h-7 w-7" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8">
        <path stroke-linecap="round" stroke-linejoin="round" d="M5.121 17.804A13.937 13.937 0 0112 16c2.5 0 4.847.655 6.879 1.804M15 10a3 3 0 11-6 0 3 3 0 016 0zm6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
    </button>

  </div>

</nav>

  );
}

export default Header;
