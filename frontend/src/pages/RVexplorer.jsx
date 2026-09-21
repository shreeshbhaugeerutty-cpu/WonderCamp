function RVexplorer() {
  return (
    <div className="bg-[#FFFFFF] text-green-800">
      {/* Navigation Bar */}
      <nav className="flex justify-evenly items-center p-4">
        <div>
          <p className="text-4xl font-bold">Wonder Camp</p>
        </div>

        <div className="relative w-full max-w-sm mx-4">
          <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-[#5B8246]">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-5 w-5"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              strokeWidth="2"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
              />
            </svg>
          </div>
          <input
            type="text"
            placeholder="Search"
            className="w-[545px] rounded-xl border border-[#366823] bg-transparent py-1.5 pl-10 pr-4 text-sm text-[#366823] placeholder-[#80a26d] focus:outline-none"
          />
        </div>

        <button>
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="h-6 w-6"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            strokeWidth="2"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7"
            />
          </svg>
        </button>

        <button>
          <div className="w-5 h-5 bg-[#326126] rounded-md relative">
            <span className="absolute -top-1 -right-1 w-2.5 h-2.5 bg-[#8BA878] rounded-full border border-[#FDFBF0]"></span>
          </div>
        </button>

        <button>
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="h-7 w-7"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            strokeWidth="1.8"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M5.121 17.804A13.937 13.937 0 0112 16c2.5 0 4.847.655 6.879 1.804M15 10a3 3 0 11-6 0 3 3 0 016 0zm6 2a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>
        </button>
      </nav>

      {/* Categories Bar */}
      <div className="border-b border-[#3B6222]/30 font-bold">
        <ul className="flex">
          <li className="mx-2 cursor-pointer hover:font-extrabold">Campsites</li>
          <li className="mx-2 cursor-pointer hover:font-extrabold">RV</li>
          <li className="mx-2 cursor-pointer hover:font-extrabold">Lodging</li>
        </ul>
      </div>

      {/* Content Grid */}
      <div className="max-w-4xl mx-auto px-8 py-10">
        <div className="grid grid-cols-2 gap-x-16 gap-y-14">
          <div className="flex flex-col items-center text-center">
            <div className="w-[280px] h-[175px] rounded-[40%] overflow-hidden">
              <img
                src="image1.png"
                alt="Class A Motorhome"
                className="w-full h-full object-cover"
              />
            </div>
            <h3 className="mt-5 text-[19px] font-serif font-bold text-[#1a1a1a] tracking-tight">
              Class A Motorhomes RV
            </h3>
            <p className="mt-1 text-[#3f7d3a] font-semibold text-[13px]">
              High luxury RV
            </p>
          </div>

          <div className="flex flex-col items-center text-center">
            <div className="w-[280px] h-[175px] rounded-[80px] overflow-hidden">
              <img
                src="image 2.png"
                alt="Class B Motorhome"
                className="w-full h-full object-cover"
              />
            </div>
            <h3 className="mt-5 text-[19px] font-serif font-bold text-[#1a1a1a] tracking-tight">
              Class B Motorhomes RV
            </h3>
            <p className="mt-1 text-[#3f7d3a] font-semibold text-[13px]">
              Medium luxury RV
            </p>
          </div>

          <div className="flex flex-col items-center text-center">
            <div className="w-[280px] h-[175px] rounded-[80px] overflow-hidden">
              <img
                src="image 3.png"
                alt="Class C Motorhome"
                className="w-full h-full object-cover"
              />
            </div>
            <h3 className="mt-5 text-[19px] font-serif font-bold text-[#1a1a1a] tracking-tight">
              Class C Motorhomes RV
            </h3>
            <p className="mt-1 text-[#3f7d3a] font-semibold text-[13px]">
              Medium luxury RV
            </p>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-[#326126] text-white py-12 px-8">
        <div className="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="w-full">
            <h1 className="text-6xl pt-3 p-4">wondercamp</h1>
            <p className="px-5 py-2">
              Providing premium caravan hire, spectacular campsite guides, and
              beautiful sightseeing spots since 2017.
            </p>
          </div>

          <div>
            <h2 className="font-bold mb-2">Explore</h2>
            <ul className="space-y-1">
              <li>
                <a href="#" className="hover:underline">
                  Mauritius Map
                </a>
              </li>
              <li>
                <a href="#" className="hover:underline">
                  All Campsites
                </a>
              </li>
              <li>
                <a href="#" className="hover:underline">
                  RV hire
                </a>
              </li>
            </ul>
          </div>

          <div>
            <h2 className="font-bold">Follow our social media</h2>
            <div className="flex flex-row pt-4">
              <a href="https://www.instagram.com/">
                <img
                  src="insta"
                  alt="Instagram"
                  className="w-10 h-10 m-2 object-cover transition-transform duration-300"
                />
              </a>
              <a href="https://www.tiktok.com/">
                <img
                  src="tiktok"
                  alt="TikTok"
                  className="w-10 h-10 m-2 object-cover transition-transform duration-300"
                />
              </a>
              <a href="https://www.linkedin.com/feed/">
                <img
                  src="linkedin"
                  alt="LinkedIn"
                  className="w-10 h-10 m-2 object-cover transition-transform duration-300"
                />
              </a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default RVexplorer;