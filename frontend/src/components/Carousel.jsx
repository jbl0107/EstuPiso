import React from 'react'


import 'slick-carousel/slick/slick.css';
import 'slick-carousel/slick/slick-theme.css';
import 'slick-carousel';
import Slider from "react-slick";



export const Carousel = () => {


    var settings = {
        dots: true,
        infinite: true,
        speed: 500,
        slidesToShow: 3,
        slidesToScroll: 3,
        initialSlide: 0,
        autoplay: true,
        autoplaySpeed: 1700,
        responsive: [
          {
            breakpoint: 1024,
            settings: {
              slidesToShow: 3,
              slidesToScroll: 3,
              infinite: true,
              dots: true
            }
          },
          {
            breakpoint: 600,
            settings: {
              slidesToShow: 2,
              slidesToScroll: 2,
              initialSlide: 2
            }
          },
          {
            breakpoint: 480,
            settings: {
              slidesToShow: 1,
              slidesToScroll: 1
            }
          }
        ]
      };


  return (
    

<div className='text-white p-20 h-screen'>
    

        <Slider {...settings}>
          <div className='h-[300px] '>
            <img src='./Imagen 1.jpg' className= 'w-full h-full' alt='Imagen 1'/>
          </div>
          <div className='h-[300px]'>
            <img src='./Imagen 2.jpg' className= 'w-full h-full' alt='Imagen 2'/>
          </div>
          <div className='h-[300px]'>
            <img src='./Imagen 3.jpg' className= 'w-full h-full' alt='Imagen 3'/>
          </div>
          <div className='h-[300px]'>
            <img src='./Imagen 4.jpg' className= 'w-full h-full' alt='Imagen 4'/>
          </div>
          <div className='h-[300px]'>
            <img src='./Imagen 5.jpg' className= 'w-full h-full' alt='Imagen 5'/>
          </div>
          <div className='h-[300px]'>
            <img src='./Imagen 6.jpg' className= 'w-full h-full' alt='Imagen 6'/>
          </div>
          <div className='h-[300px]'>
            <img src='./Imagen 7.jpg' className= 'w-full h-full' alt='Imagen 7'/>
          </div>
          <div className='h-[300px]'>
            <img src='./Imagen 8.jpg' className= 'w-full h-full' alt='Imagen 8'/>
          </div>
        </Slider>
      </div>

    
  );
}
