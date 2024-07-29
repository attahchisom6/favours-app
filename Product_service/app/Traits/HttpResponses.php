<?php

namespace App\Traits;

trait HttpResponses
{
    protected function success($message, $data, $code = 200)
    {
        return response()->json([
            'status' => true,
            'message' => $message,
            'data' => $data, 
            'code' => $code
        ], $code);
    }


    protected function error($error, $code)
    {
        return response()->json([
            "status" => false,
            "message" => $error,
            "data" => [], 
            "code" => $code
        ], $code);
    }
}
