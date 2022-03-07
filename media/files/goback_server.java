import java.net.*;
import java.util.*;
import java.io.*;

class goback_server
{
	public static void main(String[] args) throws Exception
	{
		ServerSocket ss=new ServerSocket(9090);
		int count=0;
		
		while(true)
		{
			try{
				
				count++;
				Socket s=ss.accept();
				System.out.println("Client "+count+" Connected.");
				simple cs=new simple(s,count);
				cs.start();
				
			}
			catch(Exception e)
			{
				System.out.println(e);
			}
		}
	}
}

class simple extends Thread
{
	int count;
	Socket s;
	simple(Socket ss,int count)
	{
		this.s=ss;
		this.count=count;
	}
	public void run()
	{
		while(true)
		{
			try{
				
				BufferedReader br=new BufferedReader(new InputStreamReader(s.getInputStream()));
				String str=br.readLine();
				int m=Integer.parseInt(str);

				if(m==0)
				{
					String msg="All Frame's received By Receiver ";
					System.out.println("Client "+count+" Exit!");
					System.out.println("All Frame's Received.");
					PrintWriter pw=new PrintWriter(s.getOutputStream());
					pw.println(msg);
					pw.flush();
					break;
					
				}
				else
				{
					if(m<0)
					{
						String msg="Frame "+m+" Acknowledgement Received ";
						//System.out.println(m+" Frame Received. ");
						Thread.sleep(1000);
						PrintWriter pw=new PrintWriter(s.getOutputStream());
						pw.println(msg);
						pw.flush();
					}
					else
					{
					
						String msg="Frame "+m+" Acknowledgement Received ";
						System.out.println(m+" Frame Received. ");
						Thread.sleep(1000);
						PrintWriter pw=new PrintWriter(s.getOutputStream());
						pw.println(msg);
						pw.flush();
					}
				}
			}
			catch(Exception e)
			{
				System.out.println(e);
			}
		}
	}
}

