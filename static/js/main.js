var handler;

// A $( document ).ready() block.
$( document ).ready(function() {
	handler = Plaid.create({
            apiVersion: 'v2',
            clientName: 'Plaid Walkthrough Demo',
            env: PLAID_ENVIRONMENT,
            product: ['transactions'],
            key: PLAID_PUBLIC_KEY,
            onSuccess: function(public_token) {
                $.post('/get_access_token', {public_token: public_token}, function() {
                    $('#container').fadeOut('fast', function() {
                        $('#intro').hide();
                        $('#app, #steps').fadeIn('slow');
                    });
                });
            },
        });

    $('#get-transactions-btn').on('click', function(e) {
      $.post('/transactions', function(data) {
        if (data.error != null) {
          // Format the error
          var errorHtml = '<div class="inner"><p>' +
           '<strong>' + data.error.error_code + ':</strong> ' +
           data.error.error_message + '</p></div>';
          if (data.error.error_code === 'PRODUCT_NOT_READY') {
            // Add additional context for `PRODUCT_NOT_READY` errors
            errorHtml += '<div class="inner"><p>The PRODUCT_NOT_READY ' +
             'error is returned when a request to retrieve Transaction data ' +
             'is made before Plaid finishes the <a href="https://plaid.com/' +
             'docs/quickstart/#transaction-data-with-webhooks">initial ' +
             'transaction pull.</a></p></div>';
          }
          // Render the error
          $('#get-transactions-data').slideUp(function() {
            $(this).slideUp(function() {
              $(this).html(errorHtml).slideDown();
            });
          });
        } else {
          $('#get-transactions-data').slideUp(function() {
            var html = '';
            data.transactions.forEach(function(txn, idx) {
              html += '<div class="inner">';
              html += '<strong>' + txn.name + '</strong><br>';
              html += '$' + txn.amount;
              html += '<br><em>' + txn.date + '</em>';
              html += '</div>';
            });
            $(this).slideUp(function() {
              $(this).html(html).slideDown();
            });
          });
        }
      });
	});

	$('#signin').modal({backdrop: 'static', keyboard: false})
	$( "#signin-btn" ).click( function() { signIn(); });
	$('#signin').modal('show');
});

var signIn = function() { 
	//handler.open();
	username = $( "#userName" ).val();
	if (username != "") { 
		$("#user").html("Welcome, " + "<strong>" + username + "</strong>");
		$('#signin').modal('hide');
		var ctx = $("#canvas");
		var myChart = new Chart(ctx, config);
	};

};
