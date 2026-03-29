<?php

namespace App\Controller;

use App\Exception\ApiResponseException;
use Symfony\Bundle\FrameworkBundle\Console\Application;
use Symfony\Component\Console\Input\ArrayInput;
use Symfony\Component\Console\Output\BufferedOutput;
use Symfony\Component\HttpKernel\KernelInterface;
use Symfony\Component\Routing\Annotation\Route;

class IndexController extends BaseController
{
    /**
     * @Route("/index", name="index")
     *
     * @throws ApiResponseException
     */
    public function index(KernelInterface $kernel)
    {
        $application = new Application($kernel);
        $application->setAutoExit(false);

        $input = new ArrayInput([
//            'command' => 'app:clean-old-files',
            'command' => 'app:segment-import',
//            'command' => 'app:fix-failed-segment',
//            '--segment-type' => 'GRILL',
            '--segment-type' => 'QUICK_SNACK',
        ]);
        $output = new BufferedOutput();

        $application->run($input, $output);

//        $content = $output->fetch();

        return $this->createApiResponse("Hello world");
    }
}
