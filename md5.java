/*
 * MD5
 */

import java.security.MessageDigest;
import java.math.BigInteger;

class IS_5 {

    public static String getMd5(String input)
    {
        String res = null;
        try {
            MessageDigest md = MessageDigest.getInstance("MD5");
            byte[] messageDigest = md.digest(input.getBytes());
            BigInteger no = new BigInteger(1, messageDigest);
            String output = no.toString(16);
            return output;
        } catch (Exception e) {
            e.printStackTrace();
        }
        return res;
    }

    public static void main(String args[]) {
        System.out.println("Hello");
        System.out.println(getMd5("Hello"));
    }

}