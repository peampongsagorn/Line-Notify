#region Namespaces
using System;
using System.Net;
using System.IO;
using Microsoft.SqlServer.Dts.Runtime;
#endregion

namespace ST_478a81d364d5492da747046decfc9c78
{
    /// <summary>
    /// ScriptMain is the entry point class of the script.  Do not change the name, attributes,
    /// or parent of this class.
    /// </summary>
    [Microsoft.SqlServer.Dts.Tasks.ScriptTask.SSISScriptTaskEntryPointAttribute]
    public partial class ScriptMain : Microsoft.SqlServer.Dts.Tasks.ScriptTask.VSTARTScriptObjectModelBase
    {
        public void Main()
        {
            // Assign system variables to SSIS variables
            string errorDescription = Dts.Variables["System::ErrorDescription"].Value.ToString();
            string sourceName = Dts.Variables["System::SourceName"].Value.ToString();
            string executionInstanceGUID = Dts.Variables["System::ExecutionInstanceGUID"].Value.ToString();
            string packageName = Dts.Variables["System::PackageName"].Value.ToString();

            // Construct the message to send
            string message = $"Place Job Name Here\n" +
                             $"Package Name: {packageName}\n" +
                             $"Error Description: {errorDescription}\n" +
                             $"Source Name: {sourceName}\n" +
                             $"Execution Instance GUID: {executionInstanceGUID}";

            // Send the message to Line Notify
            SendLineNotify(message);

            Dts.TaskResult = (int)ScriptResults.Success;
        }

        private void SendLineNotify(string message)
        {
            // Enable TLS 1.2
            ServicePointManager.SecurityProtocol = SecurityProtocolType.Tls12;

            string lineToken = "Place Line Notify Here"; // Replace with your actual Line Notify token
            string url = "https://notify-api.line.me/api/notify";

            WebRequest request = WebRequest.Create(url);
            request.Method = "POST";
            request.Headers.Add("Authorization", "Bearer " + lineToken);
            request.ContentType = "application/x-www-form-urlencoded";

            string postData = "message=" + Uri.EscapeDataString(message);
            byte[] byteArray = System.Text.Encoding.UTF8.GetBytes(postData);
            request.ContentLength = byteArray.Length;

            using (Stream dataStream = request.GetRequestStream())
            {
                dataStream.Write(byteArray, 0, byteArray.Length);
            }

            WebResponse response = request.GetResponse();
            using (Stream responseStream = response.GetResponseStream())
            {
                using (StreamReader reader = new StreamReader(responseStream))
                {
                    string responseFromServer = reader.ReadToEnd();
                    // Handle response if needed
                }
            }
            response.Close();
        }

        #region ScriptResults declaration
        /// <summary>
        /// This enum provides a convenient shorthand within the scope of this class for setting the
        /// result of the script.
        /// 
        /// This code was generated automatically.
        /// </summary>
        enum ScriptResults
        {
            Success = Microsoft.SqlServer.Dts.Runtime.DTSExecResult.Success,
            Failure = Microsoft.SqlServer.Dts.Runtime.DTSExecResult.Failure
        };
        #endregion
    }
}