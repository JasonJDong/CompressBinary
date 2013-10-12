using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CompressBinary
{
    class Program
    {
        static void Main(string[] args)
        {
            //var file = Path.Combine(Environment.CurrentDirectory, "1.txt");
            var file = Path.Combine(Environment.CurrentDirectory, @"D:\gzip.gz");
            using (var fs = new FileStream(file, FileMode.Open, FileAccess.Read))
            {
                var buffer = new byte[65535];
                var read = fs.Read(buffer, 0, buffer.Length);
                var bigBuffer = new List<byte>(65535 * 1024);
                while (read > 0)
                {
                    var tempBuffer = new byte[read];
                    Array.Copy(buffer, 0, tempBuffer, 0, read);
                    bigBuffer.AddRange(tempBuffer);
                    buffer = new byte[65535];
                    read = fs.Read(buffer, 0, buffer.Length);
                }
                bigBuffer.TrimExcess();
                var realRead = bigBuffer.ToArray();
                Compressor compressor = new Compressor();
                var isCompress = false;
                var compressed = compressor.SmallCompress(realRead, out isCompress);
                if (isCompress)
                {
                    var watch = new Stopwatch();
                    byte[] decompress = null;
                    watch.Start();
                    for (int i = 0; i < 1; i++)
                    {
                        decompress = compressor.SmallDecompress(compressed);
                        watch.Stop();
                        //Console.WriteLine("time:" + watch.ElapsedMilliseconds + "ms");
                        watch.Reset();
                        watch.Start();
                    }
                    //Console.WriteLine("time:" + watch.ElapsedMilliseconds + "ms");
                    for (int i = 0; i < decompress.Length; i++)
                    {
                        if (decompress[i] != realRead[i])
                        {
                            Console.WriteLine("Not Equals");
                        }
                    }
                }
                if (realRead.Length != 0)
                {
                    Console.WriteLine("Compress: " + (100 - (compressed.Length * 100.0 / realRead.Length)) + "%");
                }

                var gZipCompress = new GZipCompress();
                var gzipBytes = gZipCompress.Compress(realRead);
                Console.WriteLine("Compress: " + (100 - (gzipBytes.Length * 100.0 / realRead.Length)) + "%");
                Console.ReadKey();

            }
        }
    }
}
