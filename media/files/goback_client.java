import java.util.*;
import java.io.*;
import java.net.*;

class goback_client
{
	public static void main(String[] args) throws Exception
	{
		Scanner se=new Scanner(System.in);
		
		Socket s=new Socket("localhost",9090);
		//String str="";
		System.out.println("How many frame's Do you want to send ?");
		int str=se.nextInt();
		int flag=0,f=0;
		str++;
		System.out.println("Which Frame Do you want to lost ?");
		int lost=se.nextInt();
		for(int i=1;i<=str;i++)
		{
				if(f==1)
				{
					/*System.out.println("Inside F con.");
					OutputStreamWriter ow=new OutputStreamWriter(s.getOutputStream());
					PrintWriter pw=new PrintWriter(ow);
					pw.println(0);
					pw.flush();
					BufferedReader br=new BufferedReader(new InputStreamReader(s.getInputStream()));
					String msg=br.readLine();
					System.out.println(msg);*/
					break;
				}
				if(i==str)
				{
					//System.out.println("Inside i==str ");
					OutputStreamWriter ow=new OutputStreamWriter(s.getOutputStream());
					PrintWriter pw=new PrintWriter(ow);
					pw.println(0);
					pw.flush();
					BufferedReader br=new BufferedReader(new InputStreamReader(s.getInputStream()));
					String msg=br.readLine();
					System.out.println(msg);
					break;
				}
				else if(flag==0)
				{
					if(i==lost)
					{
						OutputStreamWriter ow=new OutputStreamWriter(s.getOutputStream());
						PrintWriter pw=new PrintWriter(ow);
						pw.println(-1);
						pw.flush();
						flag=lost;
						BufferedReader br=new BufferedReader(new InputStreamReader(s.getInputStream()));
						String msg=br.readLine();
						//System.out.println(msg);
						continue;
						
					}
					else
					{
						OutputStreamWriter ow=new OutputStreamWriter(s.getOutputStream());
						PrintWriter pw=new PrintWriter(ow);
						System.out.println("Frame "+i+" Sent.");
						pw.println(i);
						pw.flush();
						BufferedReader br=new BufferedReader(new InputStreamReader(s.getInputStream()));
						String msg=br.readLine();
						System.out.println(msg);
					}
					
					
				}
				if(flag>0)
				{
					//System.out.println("Inside Flag If..");
					f=1;
					//System.out.println("Flag Is "+flag);
					for(int j=flag;j<=str;j++)
					{
						if(j==str)
						{
							OutputStreamWriter ow=new OutputStreamWriter(s.getOutputStream());
							PrintWriter pw=new PrintWriter(ow);
							pw.println(0);
							pw.flush();
							BufferedReader br=new BufferedReader(new InputStreamReader(s.getInputStream()));
							String msg=br.readLine();
							System.out.println(msg);
							break;
						}
						else
						{

							
								OutputStreamWriter ow=new OutputStreamWriter(s.getOutputStream());
								PrintWriter pw=new PrintWriter(ow);
								System.out.println("Frame "+j+" Resending..");
								pw.println(j);
								pw.flush();
							
							
							BufferedReader br=new BufferedReader(new InputStreamReader(s.getInputStream()));
							String msg=br.readLine();
							System.out.println(msg);
						}
					}
				}
				else
				{
					continue;
				}
				
		}
		
	}
}