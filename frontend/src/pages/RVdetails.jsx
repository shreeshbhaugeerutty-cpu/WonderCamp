function RVDetails() {
  return (
    <div className="min-h-screen bg-[#eef0e6] flex justify-center p-4 text-[#366823]">
      <div className="w-full max-w-[390px] self-start bg-[#FEFBE9] rounded-md overflow-hidden pb-8">
        {/* Photo */}
        <img
          src="imageb1.png"
          alt="Class A Motorhome"
          className="w-full h-[210px] object-cover"
        />

        {/* Title + Price */}
        <div className="flex justify-between items-center px-5 mt-5">
          <h1 className="bg-[#326126] text-white text-[15px] font-bold px-4 py-2 rounded-full">
            Class A Motorhomes RV
          </h1>
          <p className="text-[15px] font-bold">
            Rs 9,990<span className="text-[9px] font-medium">/day</span>
          </p>
        </div>

        {/* Info + Book Now */}
        <div className="flex justify-between items-start px-5 mt-4">
          <div className="flex flex-col gap-2 text-[11px] font-semibold">
            <div className="flex items-center gap-1.5">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-4 w-4"
                fill="currentColor"
                viewBox="0 0 24 24"
              >
                <path d="M4 16c0 .9.4 1.7 1 2.2V20a1 1 0 001 1h1a1 1 0 001-1v-1h8v1a1 1 0 001 1h1a1 1 0 001-1v-1.8c.6-.5 1-1.3 1-2.2V6c0-3.5-3.6-4-8-4S4 2.5 4 6zm3.5 1a1.5 1.5 0 110-3 1.5 1.5 0 010 3m9 0a1.5 1.5 0 110-3 1.5 1.5 0 010 3M6 11V6h12v5z" />
              </svg>
              <p>High luxury RV</p>
            </div>

            <div className="flex items-center gap-4">
              <a href="tel:+2305000000" className="flex items-center gap-1.5">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className="h-4 w-4"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  strokeWidth="2"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"
                  />
                </svg>
                <p>Call</p>
              </a>

              <a
                href="https://wa.me/2305000000"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-1.5"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className="h-[22px] w-[22px]"
                  viewBox="0 0 24 24"
                >
                  <rect width="24" height="24" rx="6" fill="#3b7d24" />
                  <path
                    d="M12 5.5a6.5 6.5 0 00-5.6 9.8L5.5 18.5l3.3-.9A6.5 6.5 0 1012 5.5m3.3 8.9c-.14.4-.8.75-1.1.78-.3.04-.6.2-2-.4-1.7-.7-2.8-2.5-2.9-2.6-.1-.1-.7-.9-.7-1.7s.4-1.2.6-1.4c.14-.15.3-.2.4-.2h.3c.1 0 .25 0 .35.3l.5 1.2c.05.1.1.2 0 .3l-.2.3-.25.25c-.1.1-.2.2-.1.4.1.2.5.8 1.1 1.3.7.6 1.3.8 1.5.9.2.1.3.08.4-.05l.5-.6c.1-.15.25-.1.4-.05l1.1.55c.15.07.25.1.3.2.05.1.05.5-.1.9"
                    fill="#fff"
                  />
                </svg>
                <p>Whatsapp</p>
              </a>
            </div>

            <div className="flex items-center gap-1.5">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-4 w-4"
                fill="currentColor"
                viewBox="0 0 24 24"
              >
                <path d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
              <p>6 - 7 persons</p>
            </div>
          </div>

          <div className="flex flex-col items-end gap-2.5">
            <button className="bg-[#326126] hover:bg-[#244a11] text-white text-[11px] font-bold px-5 py-2 rounded-full cursor-pointer">
              Book Now
            </button>
            {/* Stars: the gold layer's width is the rating (4.5 / 5 = 90%) */}
            <div className="relative text-[17px] leading-none tracking-wide">
              <span className="text-[#e8e5c9]">★★★★★</span>
              <span className="absolute top-0 left-0 w-[90%] overflow-hidden text-[#f7c81e]">
                ★★★★★
              </span>
            </div>
          </div>
        </div>

        <p className="px-5 mt-5 text-[10px] leading-relaxed">
          <span className="font-bold">Amenities:</span> 1 Bathroom, 4 beds, 300L
          water tank for daily use, 1 Kitchen.
        </p>

        <hr className="border-[#dfe3c4] my-6 mx-5" />

        {/* Price Trends */}
        <div className="px-5">
          <h2 className="text-[10px] font-bold mb-3">
            Price trends over the past 30 days
          </h2>
          <svg viewBox="0 0 300 120" className="w-full h-auto overflow-visible">
            <defs>
             <linearGradient id="priceFill" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0" stopColor="#FEFBEB" />
              <stop offset="1" stopColor="green"  />
             </linearGradient>
           </defs>

       
            <path
              d="M14 62.7 C15.6 61.5 20.3 58.1 23.4 55.2 C26.5 52.3 29.7 45.7 32.8 45.3 C35.9 44.9 39.1 49 42.2 52.8 C45.3 56.5 48.5 63.9 51.6 67.7 C54.7 71.4 57.9 75.5 61 75.1 C64.1 74.7 67.3 68.5 70.4 65.2 C73.5 61.9 76.7 58.1 79.8 55.2 C82.9 52.3 86.1 46.5 89.2 47.8 C92.3 49 95.5 58.1 98.6 62.7 C101.7 67.3 104.9 72.2 108 75.1 C111.1 78 114.3 80.9 117.4 80.1 C120.5 79.3 123.7 74.3 126.8 70.2 C129.9 66 133.1 59.8 136.2 55.2 C139.3 50.7 142.5 43.2 145.6 42.8 C148.7 42.4 151.9 49 155 52.8 C158.1 56.5 161.3 63.9 164.4 65.2 C167.5 66.4 170.7 63.5 173.8 60.2 C176.9 56.9 180.1 49.4 183.2 45.3 C186.3 41.2 189.5 34.5 192.6 35.4 C195.7 36.2 198.9 45.3 202 50.3 C205.1 55.2 208.3 65.6 211.4 65.2 C214.5 64.8 217.7 54.4 220.8 47.8 C223.9 41.2 227.1 30.8 230.2 25.4 C233.3 20 236.5 14.2 239.6 15.5 C242.7 16.7 245.9 26.6 249 32.9 C252.1 39.1 255.3 48.2 258.4 52.8 C261.5 57.3 264.7 57.3 267.8 60.2 C270.9 63.1 274.1 66.8 277.2 70.2 C280.3 73.5 283.5 77.2 286.6 80.1 C289.7 83 294.4 86.3 296 87.6 L296 100 L14 100 Z"
              fill="url(#priceFill)"
              stroke="#3b6b1e"
              strokeWidth="1"
            />

            {/* Grid lines and axis */}
            <line x1="14" y1="8" x2="14" y2="100" stroke="#2a3a1e" strokeWidth="0.6" />
            <line x1="108" y1="8" x2="108" y2="100" stroke="#2a3a1e" strokeWidth="0.6" />
            <line x1="202" y1="8" x2="202" y2="100" stroke="#2a3a1e" strokeWidth="0.6" />
            <line x1="296" y1="8" x2="296" y2="100" stroke="#2a3a1e" strokeWidth="0.6" />
            <line x1="14" y1="100" x2="296" y2="100" stroke="#2a3a1e" strokeWidth="0.8" />

            {/* Day labels */}
            <g fontSize="9" fontWeight="700" fill="#366823">
              <text x="14" y="115" textAnchor="start">0</text>
              <text x="108" y="115" textAnchor="middle">10</text>
              <text x="202" y="115" textAnchor="middle">20</text>
              <text x="296" y="115" textAnchor="end">30</text>
            </g>
          </svg>
        </div>

        <hr className="border-[#dfe3c4] my-6 mx-5" />

        {/* Reviews */}
        <div className="px-5">
          <h2 className="text-[10px] font-bold mb-3">
            Why guests love this campsite?
          </h2>
        </div>
        <div className="flex gap-4 overflow-x-auto snap-x snap-mandatory px-5 pb-2 [scrollbar-width:none] [&::-webkit-scrollbar]:hidden">
          <div className="snap-start shrink-0 w-[82%] min-h-[150px] rounded-[56px] border border-black px-6 pt-5 pb-7">
            <div className="flex items-center gap-1.5 mb-3">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-5 w-5"
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
              <p className="text-[9px] font-bold">Theri Collinsen</p>
              <div className="relative text-[13px] leading-none">
                <span className="text-[#e8e5c9]">★★★★★</span>
                <span className="absolute top-0 left-0 w-[90%] overflow-hidden text-[#f7c81e]">
                  ★★★★★
                </span>
              </div>
            </div>
            <p className="text-[9px] leading-relaxed font-medium">
              Comfortable living while still being connected to nature. I loved
              everything about the experience, would definitely visit again.
            </p>
          </div>

          <div className="snap-start shrink-0 w-[82%] min-h-[150px] rounded-[56px] border border-black px-6 pt-5 pb-7">
            <div className="flex items-center gap-1.5 mb-3">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-5 w-5"
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
              <p className="text-[9px] font-bold">Terry Grant</p>
              <div className="relative text-[13px] leading-none">
                <span className="text-[#e8e5c9]">★★★★★</span>
                <span className="absolute top-0 left-0 w-[90%] overflow-hidden text-[#f7c81e]">
                  ★★★★★
                </span>
              </div>
            </div>
            <p className="text-[9px] leading-relaxed font-medium">
              Spotless inside, easy to drive and the host was very helpful. The
              kitchen had everything we needed for a week on the road.
            </p>
          </div>
        </div>

        <hr className="border-[#dfe3c4] my-6 mx-5" />

        {/* About / Ratings */}
        <div className="px-5">
          <h2 className="text-[10px] font-bold mb-2">About</h2>
          <div className="flex items-center gap-2 text-[11px] font-semibold mb-4">
            <p>4.5</p>
            <div className="relative text-[17px] leading-none tracking-wide">
              <span className="text-[#e8e5c9]">★★★★★</span>
              <span className="absolute top-0 left-0 w-[90%] overflow-hidden text-[#f7c81e]">
                ★★★★★
              </span>
            </div>
            <p>Good</p>
          </div>

          <div className="flex flex-col gap-3 text-[10px] font-semibold">
            <div className="grid grid-cols-[90px_1fr_28px] items-center">
              <p>Location</p>
              <div className="h-[7px] rounded-full bg-[#dcdcd4] overflow-hidden">
                <div className="h-full w-[100%] rounded-full bg-[#366823]"></div>
              </div>
              <p className="text-right">5.0</p>
            </div>

            <div className="grid grid-cols-[90px_1fr_28px] items-center">
              <p>Rooms</p>
              <div className="h-[7px] rounded-full bg-[#dcdcd4] overflow-hidden">
                <div className="h-full w-[90%] rounded-full bg-[#366823]"></div>
              </div>
              <p className="text-right">4.5</p>
            </div>

            <div className="grid grid-cols-[90px_1fr_28px] items-center">
              <p>Value</p>
              <div className="h-[7px] rounded-full bg-[#dcdcd4] overflow-hidden">
                <div className="h-full w-[82%] rounded-full bg-[#366823]"></div>
              </div>
              <p className="text-right">4.1</p>
            </div>

            <div className="grid grid-cols-[90px_1fr_28px] items-center">
              <p>Cleanliness</p>
              <div className="h-[7px] rounded-full bg-[#dcdcd4] overflow-hidden">
                <div className="h-full w-[90%] rounded-full bg-[#366823]"></div>
              </div>
              <p className="text-right">4.5</p>
            </div>

            <div className="grid grid-cols-[90px_1fr_28px] items-center">
              <p>Service</p>
              <div className="h-[7px] rounded-full bg-[#dcdcd4] overflow-hidden">
                <div className="h-full w-[98%] rounded-full bg-[#366823]"></div>
              </div>
              <p className="text-right">4.9</p>
            </div>

            <div className="grid grid-cols-[90px_1fr_28px] items-center">
              <p>Sleep Quality</p>
              <div className="h-[7px] rounded-full bg-[#dcdcd4] overflow-hidden">
                <div className="h-full w-[100%] rounded-full bg-[#366823]"></div>
              </div>
              <p className="text-right">5.0</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default RVDetails;