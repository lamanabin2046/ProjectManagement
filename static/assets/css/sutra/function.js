/* 
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */


$(document).ready(function(){
    $('.toggle').on('click', function() {
      $('.container').stop().addClass('active');
    });
    
    $('.close').on('click', function() {
      $('.container').stop().removeClass('active');
    });
    
    });
    $('.variable-width').slick({
            dots: false,
            infinite: false,
            speed: 300,
            slidesToShow: 7,
            centerMode: false,
            variableWidth: true
        });