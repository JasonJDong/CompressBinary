using System;
using System.Collections.Generic;
using System.IO;
using System.IO.Compression;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CompressBinary
{
    public class GZipCompress
    {
        public byte[] Compress(byte[] source)
        {
            //MemoryStream ms = new MemoryStream();
            FileStream fs = new FileStream(@"D:\gzip.gz", FileMode.Create, FileAccess.Write);
            // Use the newly created memory stream for the compressed data.
            GZipStream compressedzipStream = new GZipStream(fs, CompressionMode.Compress, true);
            Console.WriteLine("Compression");
            compressedzipStream.Write(source, 0, source.Length);
            // Close the stream.
            compressedzipStream.Close();
            Console.WriteLine("Original size: {0}, Compressed size: {1}", source.Length, fs.Length);
            byte[] buffer = new byte[65535];
            //ms.Read(buffer, 0, buffer.Length);
            fs.Close();
            return new byte[1];
        }
    }
}
