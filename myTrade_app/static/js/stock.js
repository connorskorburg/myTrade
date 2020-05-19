function showTotal(){
    document.getElementById('show-total').style.display = "block";
    shares = document.getElementById('shares').value;
    shares = parseFloat(shares)
    
    currentPrice = document.getElementById('current_price').innerText;
    
    function parseNumber(val, locale = 'en-US') {
      let format = Intl.NumberFormat(locale).format('1.1');
      let newPattern = new RegExp(`[^-+0-9${ format.charAt( 1 ) }]`, 'g');
      let pattern = val.replace(newPattern, '');
      let newPrice = pattern.replace(format.charAt(1), '.');
      
      return parseFloat(newPrice);
    }
    
    currentPrice = parseNumber(currentPrice);
    
    totalPrice = currentPrice * shares;
    
    accountBal = document.getElementById('account_bal').innerText;
    accountBal = parseFloat(accountBal);
    
    if(totalPrice > accountBal){
      document.getElementById('buy_btn').style.display = "none";
    }
    else if(totalPrice <= accountBal){
      document.getElementById('buy_btn').style.display = "block"
    }
    
    totalPrice = totalPrice.toFixed(2);

    document.getElementById('total_price').innerText = totalPrice;
    document.getElementById('total_shares').innerText = shares;
    document.getElementById('price_per_share').innerText = currentPrice;
    document.getElementById('input_share').value = shares;
}
