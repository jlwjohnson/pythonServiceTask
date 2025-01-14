// use Node.js to spawn a Python process with the child_process.spawn method
const { spawn } = require('child_process');

// Import Zeebe Node client
const ZB = require('zeebe-node')
// Instantiate instance of Zeebe client
const zbc = new ZB.ZBClient()
// Create and config job worker
const zbWorker = zbc.createWorker({
	taskType: 'get_risk', //defined in our workflow
	taskHandler: getRisk, //our function to run the code
})

// Function to call the Python script - this gets called from the "getRisk" function
function callPythonFunction(var1, var2, var3, var4, var5, var6, var7) {
	zbWorker.log('In function to spawn python process.')

    return new Promise((resolve, reject) => {

        zbWorker.log('Making python call, first setting blank result.')
        let result = '';

        // variables: creditScore, latePayments, monthsJob, dtiRatio, loanAmt, liquidAssets, numCC

        const pythonProcess = spawn('python', ['risk_Assessment4.py', var1, var2, var3, var4, var5, var6, var7]);
        zbWorker.log(`Spawned risk process.`)

        // Capture the script's output
        pythonProcess.stdout.on('data', (data) => {
            result += resolve(data.toString().trim());
            //zbWorker.log('Result found: ', result);
        });

        // Capture errors
        pythonProcess.stderr.on('data', (data) => {
            reject(data.toString());
        });

        pythonProcess.on('error', (error) => {
            reject(error.message);
        });

		pythonProcess.on('close', (code) => {
            if (code === 0) {
                resolve(result.trim()); // Resolve with the result on success
            } else {
                reject(`Python process exited with code ${code}`); // Handle non-zero exit codes
            }
        });
    });
}

function getRisk(job) {
	// Get process variables into your worker
	const{ creditScore, latePayments, monthsJob, dtiRatio, loanAmt, liquidAssets, numCC } = job.variables
    //zbWorker.log('Setting variables (will be passed later when function works)')
    //creditScore = 720;
	//latePayments = 2;
	//monthsJob = 12;
	//dtiRatio = 0.2314;
	//loanAmt = 125000;
    //liquidAssets = 8250;
	//numCC = 12;

	// Call the python code
    zbWorker.log(`Calling to get credit risk for credit score of: ${creditScore} and loan amount of: ${loanAmt} `)
    
    let pythonResult;

	callPythonFunction(creditScore, latePayments, monthsJob, dtiRatio, loanAmt, liquidAssets, numCC)
	    .then((result) => {
			pythonResult = result;
			zbWorker.log('Result from Python', result); // Log the result	
		})
		.catch((error) => {
			console.error('Error', error);
		});

         setTimeout(() => {
            console.log('Stored result accessed later ', pythonResult);
            zbWorker.log('Result found from python: ', pythonResult);
            zbWorker.log(`Updating the variables. . . `)

            const updateProcessVariables = {
                risk: pythonResult,
                creditScore: creditScore,
                latePayments: latePayments,
                monthsJob: monthsJob,
                dtiRatio: dtiRatio,
                loanAmt: loanAmt,
                liquidAssets: liquidAssets,
                numCC: numCC
            }

	// Complete job and send updated process variables.
	return job.complete(updateProcessVariables)
        }, 1000);  // Delay to ensure the Promise has resolved
}
